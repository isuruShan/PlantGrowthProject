#For more info [https://docs.opencv.org/trunk/d3/db4/tutorial_py_watershed.html]


from functools import wraps
from flask import (
    current_app,
    jsonify,
    request,
)

from PlantGrowthProject import app
import sys
import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt



def Compromise():
    #Detection of color green
    #START
    # load the image
    #img = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\5.JPG)
    #img = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\6.JPG") #Input the image
    image = cv2.imread("E:\\repository\\PlantGrowthProject\\PlantGrowthProject\\Test\\Capture.png")

    #Color detection Green color
    #START

    # define range of green color in RGB
    lower_green = np.array([17, 15, 100], dtype = "uint8") #60,100,50
    upper_green = np.array([50, 56, 200], dtype = "uint8") #60,255,255

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(image, lower_green, upper_green)
    output = cv2.bitwise_and(image, image, mask = mask)
    #END

    #the Otsu's binarization
    gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY) #change the color space from BGR to GRAY
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    markers = cv2.watershed(output,markers)
    output[markers == -1] = [255,0,0]

    nWhitePixels = cv2.countNonZero(thresh) #this gives number of white pixels you have in the image
    numberAll = thresh.size #this gives number of all pixels you have in the image
    print(nWhitePixels)
    print(numberAll)

    cv2.imshow("images", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print ("Tharusha shehan")
    return