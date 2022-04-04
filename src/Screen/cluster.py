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
        # *1 makes it so the cluster is twice the size as the original image (*0.5 would make them the same size)
        if (    (list_kp2[matchInScreenIndex][0] > (self.center[0] - self.width*1)) and (list_kp2[matchInScreenIndex][0] < (self.center[0] + self.width*1)) 
                and
                (list_kp2[matchInScreenIndex][1] > (self.center[1] - self.height*1)) and (list_kp2[matchInScreenIndex][1] < (self.center[1] + self.height*1)) 
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