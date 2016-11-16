#! /usr/bin/env python3
import numpy as np
import cv2

original_img = cv2.imread('data/card1.png')

# Process Image
kernel = np.ones((2,2), np.uint8)
img = cv2.morphologyEx(original_img, cv2.MORPH_OPEN, kernel)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)

# Find Contours
_, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
inner_contours = [c for c, h in zip(contours, hierarchy[0]) if h[3] == 0]

# Filter Contours by size
inner_contours=list(filter(lambda c: cv2.contourArea(c) >= 50 and cv2.contourArea(c) < original_img.size / 3, inner_contours))

# Making sure number of shapes <= 3
assert len(inner_contours) <= 3 and len(inner_contours) > 0

# Making Masks
whole_contour = np.zeros(img.shape, np.uint8)
cv2.drawContours(whole_contour, inner_contours, 0, 255, -1)
cv2.drawContours(whole_contour, inner_contours, 0, 0, 2)
contour_six = np.zeros(img.shape, np.uint8)
cv2.drawContours(contour_six, inner_contours, 0, 255, 6)
outside_shape_mask = cv2.bitwise_and(whole_contour, whole_contour, mask=contour_six)
cv2.imwrite('out/outside_shape_mask.png', outside_shape_mask)
inside_shape_mask=np.zeros(img.shape, np.uint8)
cv2.drawContours(inside_shape_mask, inner_contours, 0, 255, -1)
cv2.drawContours(inside_shape_mask, inner_contours, 0, 0, 10)
# Todo: Making sure that none of the outside mask is a part of the inside mask
# inside_shape_mask=cv2.bitwise_and(inside_shape_mask, inside_shape_mask, mask=outside_shape_mask)
cv2.imwrite('out/inside_shape_mask.png', inside_shape_mask)
bg_shape_mask=np.zeros(img.shape, np.uint8)
cv2.drawContours(bg_shape_mask, inner_contours, 0, 255, 10)
cv2.drawContours(bg_shape_mask, inner_contours, 0, 0, 8)
cv2.drawContours(bg_shape_mask, inner_contours, 0, 0, -1)
cv2.imwrite('out/bg_shape_mask.png', bg_shape_mask)

# Guess color (Works!)
hsv_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)
hue, saturation_inside = cv2.mean(hsv_img, inside_shape_mask)[0:2]
if hue >= 100 and hue <= 160:
	print("Purple")
elif hue >= 50 and hue < 100:
	print("Green")
else:
	print("Red")

# Guessing the fill
saturation_outside=cv2.mean(hsv_img, outside_shape_mask)[1]
saturation_background=cv2.mean(hsv_img, bg_shape_mask)[1]
print("Inside saturation: " + str(saturation_inside))
print("Outside saturation: " + str(saturation_outside))
print("Background saturation: " + str(saturation_background))
diff_io=abs(saturation_inside-saturation_outside)
diff_ib=abs(saturation_inside-saturation_background)
diff_ob=abs(saturation_outside-saturation_background)
if diff_io - diff_ib < 5: # Works for the 12 cards in data but more exhaustive tests preferred
	print("Open")
elif diff_ib > 10:
	print("Filled")
else:
	print("Striped")

# Guessing shape
# TODO: Fix bug. Perhaps thresholding will work
OVAL=cv2.imread("data/oval.png")
DIAMOND=cv2.imread("data/diamond.png")
SQUIGGLE=cv2.imread("data/squiggle.png")
SHAPES=[OVAL, DIAMOND, SQUIGGLE]
for shape in SHAPES:
	_, shape_contours, __ = cv2.findContours(shape, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	print(cv2.matchShapes(inner_contours[0], shape_contours[0] , 1, 0.0))
