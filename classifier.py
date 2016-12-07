#! /usr/bin/env python3
import numpy as np
import cv2

def classify(name_img):
	"""
	Doctests to make testing easier
	Use python -m doctest classifier.py
	>>> classify('card1')
	Color: Purple
	Shape: Squiggle
	Number: 1
	Fill: Open

	>>> classify('card2')
	Color: Purple
	Shape: Squiggle
	Number: 3
	Fill: Striped

	>>> classify('card3')
	Color: Green
	Shape: Oval
	Number: 1
	Fill: Open

	>>> classify('card4')
	Color: Red
	Shape: Oval
	Number: 3
	Fill: Open

	>>> classify('card5')
	Color: Purple
	Shape: Oval
	Number: 2
	Fill: Open

	>>> classify('card6')
	Color: Green
	Shape: Diamond
	Number: 3
	Fill: Striped

	>>> classify('card7')
	Color: Red
	Shape: Squiggle
	Number: 3
	Fill: Open

	>>> classify('card8')
	Color: Purple
	Shape: Diamond
	Number: 3
	Fill: Striped

	>>> classify('card9')
	Color: Red
	Shape: Squiggle
	Number: 1
	Fill: Solid

	>>> classify('card10')
	Color: Red
	Shape: Diamond
	Number: 2
	Fill: Solid
	
	>>> classify('card11')
	Color: Green
	Shape: Diamond
	Number: 1
	Fill: Solid

	>>> classify('card12')
	Color: Green
	Shape: Diamond
	Number: 2
	Fill: Solid
	"""
	original_img = cv2.imread('data/' + name_img +'.png')
	num = name_img[4:]

	# Process Image
	kernel = np.ones((2,2), np.uint8)
	img = cv2.morphologyEx(original_img, cv2.MORPH_OPEN, kernel)
	img = cv2.erode(img, kernel, iterations=4)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret,img = cv2.threshold(img, 155, 255, cv2.THRESH_BINARY)
	cv2.imwrite('out/thresh' + num + '.png', img)
	# Find Contours
	_, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	inner_contours = [c for c, h in zip(contours, hierarchy[0]) if h[3] == 0]

	# Filter Contours by size
	inner_contours=list(filter(lambda c: cv2.contourArea(c) >= 50 and cv2.contourArea(c) < original_img.size / 3, inner_contours))
	blank = np.zeros(img.shape, np.uint8)
	cv2.drawContours(blank, inner_contours, -1, 255, -1)
	cv2.imwrite('out/filter' + num + '.png', blank)

	# Making Masks
	whole_contour = np.zeros(img.shape, np.uint8)
	cv2.drawContours(whole_contour, inner_contours, 0, 255, -1)
	cv2.drawContours(whole_contour, inner_contours, 0, 0, 2)
	cv2.imwrite('out/whole_shape_mask' + num  + '.png', whole_contour)
	contour_six = np.zeros(img.shape, np.uint8)
	cv2.drawContours(contour_six, inner_contours, 0, 255, 6)
	outside_shape_mask = cv2.bitwise_and(whole_contour, whole_contour, mask=contour_six)
	cv2.imwrite('out/outside_shape_mask' + num + '.png', outside_shape_mask)
	inside_shape_mask=np.zeros(img.shape, np.uint8)
	cv2.drawContours(inside_shape_mask, inner_contours, 0, 255, -1)
	cv2.drawContours(inside_shape_mask, inner_contours, 0, 0, 10)
	# Todo: Making sure that none of the outside mask is a part of the inside mask
	# inside_shape_mask=cv2.bitwise_and(inside_shape_mask, inside_shape_mask, mask=outside_shape_mask)
	cv2.imwrite('out/inside_shape_mask'+ num + '.png', inside_shape_mask)
	bg_shape_mask=np.zeros(img.shape, np.uint8)
	cv2.drawContours(bg_shape_mask, inner_contours, 0, 255, 10)
	cv2.drawContours(bg_shape_mask, inner_contours, 0, 0, 8)
	cv2.drawContours(bg_shape_mask, inner_contours, 0, 0, -1)
	cv2.imwrite('out/bg_shape_mask'+ num + '.png', bg_shape_mask)

	# Guess color 
	cv2.imwrite('out/color_mask' + num + '.png', cv2.bitwise_and(original_img, original_img,mask=outside_shape_mask))
	print(cv2.mean(cv2.cvtColor(cv2.bitwise_and(original_img, original_img,mask=outside_shape_mask), cv2.COLOR_BGR2HSV), outside_shape_mask)[0])
	hsv_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)
	hue, saturation_inside = cv2.mean(hsv_img, outside_shape_mask)[0:2]
	print(hue)
	print("Color: ", end = '')
	if hue >= 100 and hue <= 160:
		print("Purple")
	elif hue >= 50 and hue < 100:
		print("Green")
	else:
		print("Red")

	# Guessing the fill
	saturation_outside=cv2.mean(hsv_img, outside_shape_mask)[1]
	saturation_background=cv2.mean(hsv_img, bg_shape_mask)[1]
	diff_io=abs(saturation_inside-saturation_outside)
	diff_ib=abs(saturation_inside-saturation_background)
	diff_ob=abs(saturation_outside-saturation_background)
	fill=''
	if diff_io - diff_ib < 5: 
		fill = "Open"
	elif diff_ib > 10:
		fill = "Solid"
	else:
		fill = "Striped"

	# Guessing shape
	# Read the image again
	def find_contours(img):
		ret, img = cv2.threshold(img, 127, 255, 0)
		_, contours, hierarchy = cv2.findContours(img, 2, 1)
		return contours[0]

	squiggle = cv2.imread('data/squiggle.png',0)
	oval = cv2.imread('data/oval.png', 0)
	diamond = cv2.imread('data/diamond.png', 0)
	img = cv2.imread('data/' + name_img +'.png',0)

	ret, img = cv2.threshold(img, 127, 255, 0)
	_, contours, hierarchy = cv2.findContours(img, 2, 1)
	try:
		in_contours = [c for c, h in zip(contours, hierarchy[0]) if h[3] == 0]
		in_contours=list(filter(lambda c: cv2.contourArea(c) >= 50 and cv2.contourArea(c) < original_img.size / 3, in_contours))
		img = in_contours[0]
	except IndexError:
		#print(hierarchy)
		#print(contours)
		pass
	oval = find_contours(oval)
	squiggle = find_contours(squiggle)
	diamond = find_contours(diamond)
	shapes = [(oval, 'Oval'), (squiggle, 'Squiggle'), (diamond, 'Diamond')]
	shape = min(shapes, key = lambda x: cv2.matchShapes(x[0], img, 1, 0.0))[1]
	print("Shape: " + shape)
	print("Number: " + str(len(inner_contours)))
	print("Fill: " + fill)

