# Trying to use https://docs.opencv.org/4.x/dc/dc3/tutorial_py_matcher.html
from statistics import median
from turtle import width
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import ImageGrab
import pyautogui

class Cluster:
    # constructor
    def __init__(self, templateMatches,sceneMatches,matchInScreenIndex,templateWidth, templateHeight):
        # knowing that (0,0) is top left of image, and as we go down and right, x and y increase
        # https://stackoverflow.com/questions/1680528/how-to-avoid-having-class-data-shared-among-instances
        self.matches = [] # needs to be inside to not share data between instances of class
        self.center = 0
        self.height = 0
        self.width = 0
        self.templateHeight = 0
        self.templateWidth = 0

        xdisplacement = templateWidth/2 - templateMatches[matchInScreenIndex][0]
        ydisplacement = templateHeight/2 - templateMatches[matchInScreenIndex][1]
        heightCluster = templateHeight 
        widthCluster = templateWidth
        center = [sceneMatches[matchInScreenIndex][0] + xdisplacement   ,   sceneMatches[matchInScreenIndex][1] + ydisplacement]
        
        self.templateHeight = templateHeight
        self.templateWidth = templateWidth

        self.center = center
        self.height = heightCluster
        self.width = widthCluster

        self.matches.append(matchInScreenIndex)

    def addToClusterIfBelongs(self, matchInScreenIndex,list_kp2):
        #print(list_kp2[matchInScreenIndex], self.center, self.height/2)
        #print((list_kp2[matchInScreenIndex][0] > (self.center[0] - self.width/2)), end=" ")
        #print((list_kp2[matchInScreenIndex][0] < (self.center[0] + self.width/2)), end=" ")
        #print((list_kp2[matchInScreenIndex][1] > (self.center[1] - self.height/2)), end=" ")
        #print((list_kp2[matchInScreenIndex][1] < (self.center[1] + self.height/2)), end=" ")
        if (    (list_kp2[matchInScreenIndex][0] > (self.center[0] - self.width/2)) and (list_kp2[matchInScreenIndex][0] < (self.center[0] + self.width/2)) 
                and
                (list_kp2[matchInScreenIndex][1] > (self.center[1] - self.height/2)) and (list_kp2[matchInScreenIndex][1] < (self.center[1] + self.height/2)) 
            ):
            self.matches.append(matchInScreenIndex)
            #increase cluster size
            #if (list_kp2[matchInScreenIndex][0] > )
            return True
        return False

    def clusterSize(self):
        return len(self.matches)

    def medianPoint(self,list_kp2):
        xSum = 0
        ySum = 0
        for match in self.matches:
            xSum += list_kp2[match][0]
            ySum += list_kp2[match][1]
        xMedian = xSum/len(self.matches)
        yMedian = ySum/len(self.matches)
        return [xMedian,yMedian]

    # when print is called
    def __str__(self):
        return str(self.center) + ", " + str(self.height) + ", " + str(self.width) + " | " + str(self.matches)

def addToACluster(clusters, matchInScreenIndex,list_kp2):
    for cluster in clusters:
        if (cluster.addToClusterIfBelongs(matchInScreenIndex,list_kp2) == True):
            return True
    return False

'''    def matchCluster(templateMatches, sceneMatches, matchInScreenIndex):
        # knowing that (0,0) is top left of image, and as we go down and right, x and y increase
        xdisplacement = templateWidth/2 - templateMatches[matchInScreenIndex][0]
        ydisplacement = templateHeight/2 - templateMatches[matchInScreenIndex][1]
        heightCluster = templateHeight 
        widthCluster = templateWidth
        center = [sceneMatches[matchInScreenIndex][0] + xdisplacement   ,   sceneMatches[matchInScreenIndex][0] + ydisplacement]
        return [center, heightCluster, widthCluster] #center, heightCluster, widthCluster'''


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
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)

img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

#plt.imshow(img3,),plt.show()



# https://stackoverflow.com/questions/41504686/opencv-attributeerror-list-object-has-no-attribute-queryidx
good = []
for m,n in matches :
    if m.distance < 0.7*n.distance :
        good.append(m)

# Initialize lists
list_kp1 = []
list_kp2 = []

# For each match...
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
    list_kp1.append((x1, y1))
    list_kp2.append((x2, y2))

#diferencex = list_kp2[0][0] - list_kp1[0][0]
#diferencey = list_kp2[0][1] - list_kp1[0][1]

# they're in order match for match
print("list_kp1")
print(list_kp1)
print("list_kp2")
print(list_kp2)

#for stuff in list_kp2:
#    print(stuff[0] - diferencex, end = " ")
#    print(stuff[1] - diferencey, end = " ")


#looking for clusters:
clusters = []
print("len =" + str(len(list_kp2)))
for matchInScreenIndex in range(0,len(list_kp2)):
    '''if (addToACluster(clusters, matchInScreenIndex,list_kp2) == False):
        # cluster: [[[center],[height],[width]],[all the matches in it]]
        print("+",end=" ")
        boy = Cluster(list_kp1,list_kp2,matchInScreenIndex,templateWidth, templateHeight)
        clusters.append(boy)
        print("cluster created!")
    else: 
        print("=",end=" ")
    print("--------------------")
    for cluster in clusters:
        print(cluster)
    print("--------------------")'''

    if all(cluster.addToClusterIfBelongs(matchInScreenIndex,list_kp2) == False for cluster in clusters):        
        # cluster: [[[center],[height],[width]],[all the matches in it]]
        clusters.append(Cluster(list_kp1,list_kp2,matchInScreenIndex,templateWidth, templateHeight))

for cluster in clusters:
    print(cluster)

# press the right cluster:
for i in range(0,len(clusters)):
    if (i == 0):
        biggestCluster = clusters[i]
    else:
        if (clusters[i].clusterSize() > biggestCluster.clusterSize()):
            biggestCluster = clusters[i]
zoomer = biggestCluster.medianPoint(list_kp2)
pyautogui.click(zoomer[0],zoomer[1])


plt.imshow(img3,),plt.show()

'''
# clicking in median point
xSum = 0
ySum = 0
for matchInScreen in list_kp2:
    xSum += matchInScreen[0]
    ySum += matchInScreen[1]
xMedian = xSum/len(list_kp2)
yMedian = ySum/len(list_kp2)
pyautogui.click(x=xMedian, y=yMedian)
'''

