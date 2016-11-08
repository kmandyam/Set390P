#! /usr/bin/env python3
import numpy as np
import cv2

original_img = cv2.imread('data/card7.png')

# Process Image
kernel = np.ones((2,2), np.uint8)
img = cv2.morphologyEx(original_img, cv2.MORPH_OPEN, kernel)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

# Find Contours
img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_ = [c for c, h in zip(contours, hierarchy[0]) if h[3] == 0]

count_ = len(contours_)
print(count_)

whole_shape = np.zeros(img.shape, np.uint8)
cv2.drawContours(whole_shape, contours_, 0, 255, -1)
cv2.drawContours(whole_shape, contours_, 0, 0, 2)
cv2.imwrite('out/contours.png', whole_shape)
cv2.imwrite('out/card1.png', img)
