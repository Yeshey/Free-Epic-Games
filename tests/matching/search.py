# Trying to use https://stackoverflow.com/questions/27343997/using-pil-python-image-library-to-detect-image-on-screen# USAGE
# python match.py --template cod_logo.png --images images
# USAGE2 Understand the actual detection principle and details 
# python match.py --template cod_logo.png --images images --visualize 1
# Import necessary packages 
import argparse # argparse Parsing command line arguments 
import glob # Get the path of the input image 
import cv2 # opencv binding 
import imutils # Some methods of image processing 
import PIL
from PIL import ImageGrab
import numpy as np
from pandas import array # numpy Perform numerical processing 

'''
img1 = cv2.imread("screenshot.png", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("FREENOW.png", cv2.IMREAD_GRAYSCALE)

# detecting keypoints
detector = cv2.FastFeatureDetector(15)
keypoints1 = list()
kp = detector.detect("FREENOW.png",keypoints1)

#vector<KeyPoint> keypoints1;-

#detector.detect(img1, keypoints1)

#... // do the same for the second image
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('screenshot.png',0)


# Initiate FAST object with default values
fast = cv2.FastFeatureDetector()

# find and draw the keypoints
kp = fast.detect(img,None)
img2 = cv2.drawKeypoints(img, kp, color=(255,0,0))

# Print all default params
print ("Threshold: ", fast.getInt('threshold'))
print ("nonmaxSuppression: ", fast.getBool('nonmaxSuppression'))
print ("neighborhood: ", fast.getInt('type'))
print ("Total Keypoints with nonmaxSuppression: ", len(kp))

cv2.imwrite('fast_true.png',img2)

# Disable nonmaxSuppression
fast.setBool('nonmaxSuppression',0)
kp = fast.detect(img,None)

print ("Total Keypoints without nonmaxSuppression: ", len(kp))

img3 = cv2.drawKeypoints(img, kp, color=(255,0,0))

cv2.imwrite('fast_false.png',img3)