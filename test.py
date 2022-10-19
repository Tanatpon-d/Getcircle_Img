from tkinter import Y
import requests
from PIL import Image
import cv2 as cv
import numpy as np


url = 'https://prepro.informatics.buu.ac.th/formalinapp_api/upload'
image = cv.imread('formalin400.png')
output = image.copy()
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# detect circles in the image
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1.2, 100)
# ensure at least some circles were found
(h, w) = image.shape[:2]
# where w//2, h//2 are the required frame/image centeroid's XYcoordinates.
cv.circle(image, (w//2, h//2), 7, (255, 255, 255), -1)

print(w//2,h//2)

if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv.circle(output, (x, y), r, (0, 255, 0), 4)
        cv.rectangle(output, (x - 5, y - 5),
                      (x + 5, y + 5), (0, 128, 255), -1)
        print(r)
    # show the output image
    cv.imshow("output", np.hstack([image, output]))
    cv.waitKey(0)
