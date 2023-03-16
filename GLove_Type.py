import cv2
import numpy as np
import requests
import imutils

def f(x):
    return 0

def glove_type():
    url = "https://192.168.100.67:8080/shot.jpg"
    cap = cv2.VideoCapture(0)
    threshType = cv2.THRESH_BINARY_INV
    threshVal = 100

    trackbarCreated = False
    while True:
        ret,frame = cap.read()
        img_resp = requests.get(url, verify=False)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        frame = imutils.resize(img, width=1000, height=1800)
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)


        r, thresh = cv2.threshold(gray, threshVal, 255, threshType)

        contours, hierarchy = cv2.findContours(thresh, method=cv2.RETR_TREE,
                                               mode=cv2.CHAIN_APPROX_NONE)  # method does not impact. mode can be NONE
        # contours = max(contours, key = lambda x: cv2.contourArea(x))
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if (area >= 7000):
                cv2.drawContours(frame,[cnt],-1,(0,0,255),2)
                hull = cv2.convexHull(cnt)


                peri1 = cv2.arcLength(cnt, True)
                c1 = cv2.approxPolyDP(cnt, 0.02 * peri1, True)
                x1,y1,w1,h1 = cv2.boundingRect(c1)
                cv2.rectangle(cnt, (x1,y1), (x1+w1 , y1+h1), (0,255,0), 5)

                peri2 = cv2.arcLength(hull, True)
                c2 = cv2.approxPolyDP(hull, 0.02 * peri2, True)
                x2, y2, w2, h2 = cv2.boundingRect(hull)
                cv2.rectangle(hull, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 5)

                if (len(c1) == 11) & (len(c2) == 7):
                    x,y,w,h = cv2.boundingRect(cnt)
                    if (w/h >= 0.6):
                        typeText = "This is glove Type-A"
                    elif (w/h >= 0.5):
                        typeText = "This is glove Type-B"
                    else:
                        typeText = "This is glove Type-C"
                    cv2.putText(frame, typeText, (x1 + w1 + 20, y1 + 20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
                    cv2.drawContours(frame, [c2], -1, (255, 0, 0), 2)
                    cv2.drawContours(frame,[c1],-1,(0,255,0),2)
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),1)


        # cv2.drawContours(frame, [hull], -1, (0, 255, 255), 2)

        # for x in contours:

        # for x in contours:
        #     area = cv2.contourArea(x)
        #     perim = cv2.arcLength(x, True)
        #     e = 0.08 * perim
        #     c1 = cv2.approxPolyDP(x, e, True)
        #     cv2.drawContours(frame,[c1],-1,(0,0,255),2)

        cv2.imshow("Video", frame)
        if (trackbarCreated == False):
            cv2.createTrackbar("Threshold Type", "Video", 0, 1, f)
            cv2.createTrackbar("ThreshVal", "Video", 100, 255, f)
            trackbarCreated = True
        if (cv2.getTrackbarPos("Threshold Type", "Video") == 0):
            threshType = cv2.THRESH_BINARY_INV
        else:
            threshType = cv2.THRESH_BINARY
        threshVal = cv2.getTrackbarPos("ThreshVal", "Video")
        # cv2.imshow("Gray",thresh)
        if (cv2.waitKey(1) == 13):
            break

    cap.release()
    cv2.destroyAllWindows()

#glove_type()