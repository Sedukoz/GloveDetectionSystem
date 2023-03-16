import cv2 as cv
import math
import numpy as np
def glove_detect():
    video = cv.VideoCapture(1)
    address="https://192.168.1.4:8080/video"
    video.open(address)

    # cap.set(3, frameWidth)
    # cap.set(4, frameHeight)
    # img = cv.imread("Glove_horizontal_right.jpg")
    # img = cv.flip(img, 0) #1: flipping y axis, 0: flipping x axis or -1: flipped both axes.
    #
    # if img is None:
    #     print('Input Image', img)
    #     exit(0)
    while True:
        check,frame = video.read()
        grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        threshold, bw = cv.threshold(grayscale, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

        for i, c in enumerate(contours):
            area = cv.contourArea(c)

            if area < 3700 or 100000 < area:
                continue

            # cv.minAreaRect returns:
            # (center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(c)
            rect = cv.minAreaRect(c)
            box = cv.boxPoints(rect)
            box = np.int0(box)

            # Retrieve the key parameters of the rotated bounding box
            center = (int(rect[0][0]), int(rect[0][1]))
            width = int(rect[1][0])
            height = int(rect[1][1])
            angle = int(rect[2])

            if width < height:
                angle = 90 - angle
            else:
                angle = -angle

            label = "  Rotation Angle: " + str(angle) + " degrees"
            textbox = cv.rectangle(frame, (center[0] - 35, center[1] - 25), (center[0] + 295, center[1] + 10),
                                   (255, 255, 255), -1)
            cv.putText(frame, label, (center[0] - 50, center[1]), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv.LINE_AA)
            cv.drawContours(frame, [box], 0, (0, 0, 255), 2)
        cv.imshow('Result', frame)
        key=cv.waitKey(1)

        if (cv2.waitKey(1) == 13):
            break

    # cv.imshow('Input Image', img)
    # while True:
    #     success, img = cap.read()
    #
    #     if img is None:
    #         print('Input Image', img)
    #         exit(0)

    video.release()
    cv.destroyAllWindows()

#glove_detect()