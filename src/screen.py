# Trying to use https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
from gettext import find
from statistics import median
from turtle import width
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import ImageGrab
import pyautogui
from datetime import datetime
from src.cluster import Cluster # my class
import config #my config

class Screen:
    #def __init__():
    @classmethod
    def find(self, imageToFind, minimumMatches=3 ,show=False):

        im = ImageGrab.grab()
        im.save("screenshot.png", "PNG")

        img1 = cv.imread(imageToFind,cv.IMREAD_GRAYSCALE) # queryImage
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

            # Append to each list, # they're in order match for match
            templateMatches.append((x1, y1))
            sceneMatches.append((x2, y2))

        Cluster.setMatches(templateMatches,sceneMatches) # using classmethod

        #looking for clusters:
        self.clusters = []
        for matchInScreenIndex in range(0,len(sceneMatches)):
            if all(cluster.addToClusterIfBelongs(matchInScreenIndex) == False for cluster in self.clusters):        
                self.clusters.append(Cluster(matchInScreenIndex,templateWidth, templateHeight))

        # press the right cluster:
        biggestCluster = None
        for i in range(0,len(self.clusters)):
            if (i == 0):
                biggestCluster = self.clusters[i]
            else:
                if (self.clusters[i].clusterSize() > biggestCluster.clusterSize()):
                    biggestCluster = self.clusters[i]

        if (show == True):
            plt.imshow(img3,),plt.show()

        if (biggestCluster != None and biggestCluster.clusterSize() >= minimumMatches):
            return biggestCluster.medianPointCoords()
        else:
            return None

    #@classmethod
    def wait_to_see(inimg1, inimg2=None, moveMouse = True, timeout=20, minimumMatches=3):
        if (moveMouse == True):
            pyautogui.moveTo(1,1)
        print("looking for",inimg1, end="")
        start_time = datetime.now()
        while True:
            time_delta = datetime.now() - start_time
            if time_delta.total_seconds() >= timeout:
                print("time limit exceeded")
                return None
            print(".", end="")

            #img = Screen.find(config.IMGS_FLDR+inimg1, minimumMatches, show=True)
            img = pyautogui.locateCenterOnScreen(config.IMGS_FLDR+inimg1, grayscale=True, confidence=.8)
            if img is not None:
                break 
            if (inimg2 != None):
                #img = Screen.find(config.IMGS_FLDR+inimg2, minimumMatches)
                img = pyautogui.locateCenterOnScreen(config.IMGS_FLDR+inimg2, grayscale=True, confidence=.8)
                if img is not None:
                    break 
        return img

    def __str__(self):
        for cluster in self.clusters:
            print(cluster)
