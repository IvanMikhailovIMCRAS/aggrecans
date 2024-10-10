from multiprocessing import Pool

from aggrecans import frame_calc, frame_proccesing

if __name__ == "__main__":

    params = [
        {
            "m1": 5,
            "m2": 3,
            "n1": 3,
            "n2": 3,
            "P1": 10,
            "P2": 10,
            "sigma": 100,
            "folder": "data1",
        },
        {
            "m1": 5,
            "m2": 3,
            "n1": 3,
            "n2": 3,
            "P1": 10,
            "P2": 10,          
            "sigma": 0.01,
            "folder": "data2",
        },
        {
            "m1": 10,
            "m2": 3,
            "n1": 3,
            "n2": 3,
            "P1": 10,
            "P2": 10,
            "sigma": 0.01,
            "folder": "data3",
        },
    ]

    inits = [(frame_proccesing(**x), x["folder"]) for x in params]

    with Pool(processes=4) as pool:
        for i in inits:
            pool.apply_async(frame_calc, i)

        pool.close()
        pool.join()
