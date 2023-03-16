import cv2
import numpy as np
import math

def Glove_Measure():
    frameWidth = 200
    frameHeight = 200
    videocap = cv2.VideoCapture(2)
    videocap.set(3, frameWidth)
    videocap.set(4, frameHeight)

    def empty(a):
        pass

    centers=[]

    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 640, 100)
    cv2.createTrackbar("Threshold", "Parameters", 40, 255, empty)


    def stackImages(scale,imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            ver = hor
        return ver


    def calculateDistance(x1,y1,x2,y2):
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    def gapCalculate(p1, p2):
        """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
        dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
        return dis

    def getContours(img, imgContour):
        contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area> 1000:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 100), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                # print(len(approx))
                x_, y_, w, h = cv2.boundingRect(approx)
                cv2.rectangle(imgContour, (x_ , y_), (x_ + w, y_ + h), (0, 255, 0), 1)



                p1 = (x_ + w , y_ )

                p2 = (x_ , y_ + h )

                cv2.putText(imgContour, "Obj", (x_ , y_  ), cv2.FONT_HERSHEY_SIMPLEX, .5,
                             (0, 255, 0), 2)
                p3 = (x_ , y_  )



                gapLength =(gapCalculate(p3, p2))/10
                format_gapLength = "{:.2f}".format(gapLength)

                lenghtP = int(calculateDistance(x_ ,y_  ,x_ + w,y_))/2.6
                format_lenghtP = "{:.2f}".format(lenghtP)
                WedthP = int(calculateDistance(x_ , y_  ,x_ ,y_ + h))/2.6
                format_WedthP = "{:.2f}".format(WedthP)



                cv2.putText(imgContour, "L: " + str(format_lenghtP)+'mm', (x_ + w + -10, y_ + -10), cv2.FONT_HERSHEY_SIMPLEX, .5,
                            (255, 255, 255), 2)
                cv2.putText(imgContour, "W: " + str(format_WedthP)+'mm', (x_ + w + -10, y_ + -30), cv2.FONT_HERSHEY_SIMPLEX, .5,
                            (255, 255, 255), 2)
                cv2.putText(imgContour, "G: " + str(format_gapLength)+'mm', (x_ + w + -10, y_ + -50), cv2.FONT_HERSHEY_SIMPLEX, .5,
                            (255, 255, 255), 2)




    while True:
        success, img = videocap.read()
        imgContour = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (11, 11), 1)


        threshold1 = cv2.getTrackbarPos("Threshold", "Parameters")
        imgCanny = cv2.Canny(imgGray,threshold1,255)

        kernel = np.ones((5, 5))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=3)
        imgerode = cv2.erode(imgDil,kernel,iterations=3)

        getContours(imgDil, imgContour)

        imgStack = stackImages(0.8,([img,imgGray,imgCanny],
                                    [imgDil,imgerode,imgContour]))

        cv2.imshow("Result", imgStack)
        if cv2.waitKey(1) == 13:
            break


    cv2.destroyAllWindows()





