# Trying to use https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
from statistics import median
from turtle import width
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import ImageGrab
import pyautogui
from cluster import Cluster # my class

#class Screen:
    #def __init__():
#    def find(self, imageToFind):

im = ImageGrab.grab()
im.save("screenshot.png", "PNG")

img1 = cv.imread('FREENOW1.png',cv.IMREAD_GRAYSCALE) # queryImage
img2 = cv.imread('screenshot.png',cv.IMREAD_GRAYSCALE) # trainImage

templateWidth = img1.shape[1] # get width and height of the template
templateHeight = img1.shape[0]

# Initiate SIFT detector
sift = cv.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50) # or pass empty dictionary

flann = cv.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

# ratio test as per Lowe's paper
good = []
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
        good.append(m)

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)

img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

# Initialize lists
templateMatches = []
sceneMatches = []

# For each match find the coordinates
for mat in good:
    # Get the matching keypoints for each of the images
    img1_idx = mat.queryIdx
    img2_idx = mat.trainIdx

    # x - columns
    # y - rows
    # Get the coordinates
    (x1, y1) = kp1[img1_idx].pt
    (x2, y2) = kp2[img2_idx].pt

    # Append to each list
    templateMatches.append((x1, y1))
    sceneMatches.append((x2, y2))

# they're in order match for match
print("templateMatches")
print(templateMatches)
print("sceneMatches")
print(sceneMatches)

#looking for clusters:
clusters = []
print("len =" + str(len(sceneMatches)))
for matchInScreenIndex in range(0,len(sceneMatches)):
    if all(cluster.addToClusterIfBelongs(matchInScreenIndex,sceneMatches) == False for cluster in clusters):        
        clusters.append(Cluster(templateMatches,sceneMatches,matchInScreenIndex,templateWidth, templateHeight))

for cluster in clusters:
    print(cluster)

# press the right cluster:
for i in range(0,len(clusters)):
    if (i == 0):
        biggestCluster = clusters[i]
    else:
        if (clusters[i].clusterSize() > biggestCluster.clusterSize()):
            biggestCluster = clusters[i]
zoomer = biggestCluster.medianPoint(sceneMatches)
pyautogui.click(zoomer[0],zoomer[1])

plt.imshow(img3,),plt.show()
