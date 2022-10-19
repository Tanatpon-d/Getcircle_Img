import requests
from PIL import Image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt






image = cv.imread('formalin400.png')

# detect circles in the image
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# detect circles in the image
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1.2, 100)
print(image.shape)
plt.imshow(circles)
