import warnings

import numpy as np
from sfbox_api import Composition, Frame, Lat, Mol, Mon, Sys


def brush_frame(
    m1: int,
    m2: int,
    n1: int,
    n2: int,
    P1: int,
    P2: int,
    sigma: float,
    chi: float = 0.0,
    n_layers: int = 0,
    folder: str = "",
) -> Frame:

    if n_layers == 0:
        n_layers = 1 + m1 * P1 + m2 * P2 + m2

    if m1 < 1 or m2 < 2 or n1 < 0 or n2 < 0 or P1 < 1 or P2 < 2:
        # warnings.warn("Set incorrected parameters")
        raise ValueError("Set incorrected parameters")

    # Topological script
    if n1 == 0 and n2 == 0:
        comp = f"(X)1((A){m1}){P1}(L){1}(B){m2-1}((B){m2}){P2-1}(B){m2-1}(E)1"
    elif n1 != 0 and n2 == 0:
        comp = f"(X)1((A){m1}[(A){n1}]){P1}(L){1}(B){m2-1}((B){m2}){P2-1}(B){m2-1}(E)1"
    elif n1 == 0 and n2 != 0:
        comp = f"(X)1((A){m1}){P1}(L){1}(B){m2-1}[(B){n2}]((B){m2}[(B){n2}]){P2-1}(B){m2-1}(E)1"
    else:
        comp = f"(X)1((A){m1}[(A){n1}]){P1}(L){1}(B){m2-1}[(B){n2}]((B){m2}[(B){n2}]){P2-1}(B){m2-1}(E)1"

    theta = sigma * Composition(comp).N

    lat = Lat(
        **{
            "n_layers": n_layers,
            "geometry": "flat",
            "lowerbound": "surface",
            # "upperbound": "surface",
        }
    )

    mons = [
        Mon(**{"name": "X", "freedom": "pinned", "pinned_range": "1"}),
        Mon(**{"name": "A", "freedom": "free"}),
        Mon(**{"name": "B", "freedom": "free"}),
        Mon(**{"name": "L", "freedom": "free"}),
        Mon(**{"name": "E", "freedom": "free"}),
        Mon(**{"name": "W", "freedom": "free"}),
    ]

    mols = [
        Mol(**{"name": "Water", "composition": "(W)1", "freedom": "solvent"}),
        Mol(
            **{
                "name": "pol",
                "composition": comp,
                "freedom": "restricted",
                "theta": theta,
            }
        ),
    ]

    sys = Sys()

    chi_list = {
        "X W": chi,
        "A W": chi,
        "B W": chi,
        "L W": chi,
        "E W": chi,
    }

    frame = Frame(lat, sys, mols, mons, chi_list=chi_list)
    frame.text += "sys : name : overflow_protection : true"

    return frame


def frame_proccesing(*args, **kwargs) -> Frame:

    frame = brush_frame(*args, **kwargs)

    return frame


def frame_calc(frame: Frame, folder: str) -> None:
    try:
        frame.run(folder)
        data = np.vstack(
            [
                frame.profile["layer"],
                frame.profile["pol"],
                frame.profile["L"],
                frame.profile["E"],
            ]
        )
        header = "z    phi    L    E"
        np.savetxt(f"{folder}.txt", data.T, header=header, comments="")
        print(f"{folder} is OK")
    except TimeoutError:
        warnings.warn(f"Error in {folder}")
