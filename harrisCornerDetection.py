import cv2
import numpy as np
import copy

img = cv2.imread('emptyBoardCropped.jpg')
img_orig = copy.copy(img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# must give a float32 data type input
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.4)

# result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst > 0.001 * dst.max()] = [0, 0, 255]

sift = cv2.xfeatures2d.SIFT_create(img)

cv2.imshow('Original', img_orig)

cv2.imshow('Original', sift)
cv2.imshow('Harris Corner Detector', img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()