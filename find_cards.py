#! /usr/bin/env python3
import numpy as np
from cv2 import *
from copy import * 
original_img = imread('boards/game1.png')
bg_img = cvtColor(original_img, COLOR_BGR2GRAY)

# Thresholding
ret, thresh = threshold(bg_img, 128, 255, THRESH_BINARY)
thresh2 = copy(thresh) # Prevent thresh from getting overwritten

#Find and draw contours
img, contours, hierarchy = findContours(thresh2, RETR_TREE, CHAIN_APPROX_SIMPLE)
imwrite('out/thresh2.png', thresh2)
outermost_contours = [c for c, h in zip(contours, hierarchy[0]) if h[3] ==  -1]
outermost_contours = list(filter(lambda x: contourArea(x) > 50, outermost_contours))
drawContours(thresh, outermost_contours, -1, (0,255,0), 3)
imwrite('out/contours_img.png', thresh)
drawContours(original_img, outermost_contours, -1, (0,255,0), 3)
imwrite('out/sanity_check_img.png', original_img) # Can't get green contours on thresh -_-

# Making mask
mask = np.zeros(bg_img.shape, np.uint8)
imwrite('out/mask.png', mask)
drawContours(mask, outermost_contours, 11, 255, -1)
imwrite('out/mask0.png', mask)

# Finding line segments 
edges = Canny(mask, 100, 200) # Canny edge detection
imwrite('out/edges.png', edges)
