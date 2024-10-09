from aggrecans import brush_frame

if __name__ == "__main__":
    frame = brush_frame(m1=5, m2=5, n1=3, n2=6, P1=10, P2=10, sigma=0.01, folder="data")
    # print(frame.profile_labels)
    print(frame)