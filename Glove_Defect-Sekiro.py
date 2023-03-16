import os
import cv2
import numpy as np
def glove_defect():
    font = cv2.FONT_HERSHEY_SIMPLEX

    #video capture values
    frameWidth = 200
    frameHeight = 200
    videocap = cv2.VideoCapture(1)
    videocap.set(3, frameWidth)
    videocap.set(4, frameHeight)

    IMAGE_SIZE = (500, 500)
    THRESHOLD_VALUE = 110
    MAX_VALUE = 255
    INV_THRESHOLD_VALUE = 50
    INV_MAX_VALUE = 255

    # Canny
    THRESHOLD1 = 100
    THRESHOLD2 = 70

    # Contour
    CON_COLOR = (0, 0, 255)
    CON_THICKNESS = 1

    # Text color
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)

    while(True):

        # Change variable name for different file
        #img = cv2.imread("imga.jpg")
        success, img = videocap.read()

        # converts to grayscale
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # resize image
        image = cv2.resize(image, IMAGE_SIZE)
        img = cv2.resize(img, IMAGE_SIZE)
        image = cv2.GaussianBlur(image, (3, 3), 0)
        # Threshold the image
        ret, thresh_basic = cv2.threshold(image, THRESHOLD_VALUE, MAX_VALUE, cv2.THRESH_BINARY)
        # Taking a matrix of size 5 as the kernel
        kernel = np.ones((5, 5), np.uint8)
        # Morphological operations-Erodes away the boundaries of foreground object
        # Use morphology to clean up extraneous markings.
        img_erosion = cv2.erode(thresh_basic, kernel, iterations=1)
        # The invert the thresholded image,
        # so that the black markings are white on a black background and then find the external contours of those.
        ret, thresh_inv = cv2.threshold(img_erosion, INV_THRESHOLD_VALUE, INV_MAX_VALUE, cv2.THRESH_BINARY_INV)
        # Find Canny edges
        edged = cv2.Canny(img_erosion, THRESHOLD1, THRESHOLD2)


        # Find Contours
        # findContours alters the image
        contours, hierarchy = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # get total contours
        num_of_con = str(len(contours) - 1)
        # show original img
        cv2.imshow('Original Image', img)
        # draw contours on original img
        if int(num_of_con) != 0:
            for i in range(int(num_of_con)):
                highlighted_img = cv2.drawContours(img, contours, i, CON_COLOR, CON_THICKNESS)
            highlighted_img = cv2.putText(highlighted_img, 'Approximately {} defect(s) detected'.
                                          format(num_of_con), (5, 15),
                                          font, 0.5, GREEN, 1, cv2.LINE_AA)
        else:
            highlighted_img = cv2.putText(img, 'Unable to detect defects!',
                                          (5, 15), font, 0.5, RED, 2, cv2.LINE_AA)
        # show markings highlighted img
        cv2.imshow('Highlighted Defect', highlighted_img)
        if cv2.waitKey(1) & 0xFF == 13:
            break

    cv2.destroyAllWindows()

