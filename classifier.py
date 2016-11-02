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
contours_ = []
hierarchy_ = []
for c, h in zip(contours, hierarchy):
  if cv2.contourArea(c) > 50:
    contours_.append(c)
    hierarchy_.append(h)

hierarchy_ = [list(x) for x in hierarchy_[0] if x[3] == 0]
count_ = len(hierarchy_)
print(count_)
cv2.imwrite('out/card1.png', img)
