import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import ColorSysCustom as csc
from cv2 import cv

class ImageProcessing():
    
    def __init__(self, imgString): 
        imgTemp = Image.open(imgString)
        self.height, self.width = imgTemp.size
        self.img = cv2.imread(imgString)
        self.maxSpacing = 0.0;
        
                
    # width of image, height of image, image, fraction of the image to be randomly taken pixels from            
    def getAverageLightIntensity(self, width, height, img, fractionOfImage):   
        sum = 0;
        self.n = np.int(fractionOfImage*width*height)
            
        randomsX = np.random.uniform(0, np.int(width), size = self.n)
        randomsY = np.random.uniform(0, np.int(height), size = self.n)
        
        for i in xrange(0, self.n):   
            B, G, R = img[randomsX[i]][randomsY[i]]
                
             #fitting them for HSV transform
            R = np.double(R)/255
            G = np.double(G)/255
            B = np.double(B)/255
            L = csc.rgb_to_luminance(R, G, B)
            sum = sum + L
        self.Lic = (sum/self.n)
        
    def setThreshold(self, t):
        self.threshold = t
        
    def getThreshold(self):
        return self.threshold
   
    
    def startLumi(self):    
        self.new_img = Image.new('RGB', (self.height, self.width), "black")
        #pixels = self.img.load()
        
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                B, G, R = self.img[x][y]
                #Using REC. 601 algorithm to calculate the grayscale of RGB value
                Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
                
                #Getting the Hue
                R = np.double(R)/255
                G = np.double(G)/255
                B = np.double(B)/255
                H = csc.rgb_to_hue(R, G, B)
                
                if(self.acceptedLumi(Y)):
                    self.img[x, y] = (255,255,255)
                elif(self.acceptedGreen(H)):
                    self.img[x, y] = (0,255,0)
                #elif(self.acceptedBlack(Y)):
                #    pixels[x, y] = (0,255,0)
                else:
                    self.img[x, y] = (0, 0, 0)
                    
        self.removeBackGround()

   
    def removeBackGround(self):
        
        #self.white_list = []
        w = self.getHeightImage()
        h = self.getWidthImage()
        for x in xrange(0, w):
            count = 0
            
            for y in xrange(0, h):
                B, G, R = self.img[y][x]
                if(B == 0 and G == 255 and R == 0):
                    count = count + 1
                else:
                    count = 0
                if(count > self.maxSpacing):
                    for r in xrange(0, y-count+1):
                        self.img[r, x] = (0, 0, 0)
                    break
        
        self.abstractImage()
        #self.onlyWhite()
        
    def clusterImage(self):
        clusterSize = self.getHeightImage()/20
        self.clusterpoins = []
        h = self.getWidthImage()
        samples = h*np.int(clusterSize/3)
        
        for x in xrange(0, 20):
            
            tempPoints = []
            nrClusters = 0
            
            for i in xrange(0, np.int(samples)):
                
                rx = np.random.random()*clusterSize + x*clusterSize
                ry = np.random.random()*h
                
                #check if white
                B, G, R = self.img[ry][rx]
                if (B == 255 and G == 255 and R == 255):
                    
                    #if there are no points assigned yet:
                    if (len(tempPoints) is 0):
                        tempPoints.append([0, rx, ry])
                    #else go though the individual clusters and check where it belongs to, if it doesn't belong to any, make a new cluster
                    else:
                        close = False
                        for c in xrange(0, len(tempPoints)):
                            cn, cx, cy = tempPoints[c]
                            if(np.abs(ry - cy) <= self.maxSpacing):
                                close = True
                                tempPoints.append([cn, rx, ry])
                                break
                        if(close is False):
                            nrClusters = nrClusters + 1
                            tempPoints.append([nrClusters, rx, ry])
            
            #averaging the clusterpoints and add to clusterlist
            if (len(tempPoints) is not 0):
                for i in xrange(0, nrClusters + 1):
                    xsum = 0
                    ysum = 0
                    n = 0
                    for j in xrange(0, len(tempPoints)):
                        cn, cx, cy = tempPoints[j]
                        if(cn is i):
                            n = n + 1
                            xsum = xsum + cx
                            ysum = ysum + cy
                    self.clusterpoins.append([xsum/n, ysum/n])
        self.finalizeImage()
        
    def abstractImage(self):
        
        self.clusterpoints = []
        w = self.getHeightImage()
        h = self.getWidthImage()
        
        for x in xrange(0, np.int(w)):
            whites = []
            self.y = 0
            while self.y < np.int(h):
                #check if white
                B, G, R = self.img[self.y][x]
                if (B == 255 and G == 255 and R == 255):
                    whites.append([x, self.y])
                    #if white, check next ones until there are no more whites and average the point
                    for y2 in xrange(self.y+1, np.int(h)):
                        B, G, R = self.img[y2][x]
                        if (B == 255 and G == 255 and R == 255):
                            whites.append([x, y2])
                        else:
                            self.y = y2+1
                            sumX = 0
                            sumY = 0
                            for i in xrange(0, len(whites)):
                                sumX = sumX + whites[i][1]
                                sumY = sumY + whites[i][0]
                            self.clusterpoints.append([sumX/len(whites), sumY/len(whites)])
                            whites = []
                            break
                self.y = self.y + 1
                    
        self.finalizeImage()
        
    def finalizeImage(self):
        for x in xrange(0, self.getWidthImage()):
            for y in xrange(0, self.getHeightImage()):
                self.img[x, y] = (0, 0, 0)
        for c in xrange(0, len(self.clusterpoins)):
            self.img[self.clusterpoins[c][1], self.clusterpoins[c][0]] = (255, 255, 255)
        
    def onlyWhite(self):
        for x in xrange(0, self.getWidthImage()):
            for y in xrange(0, self.getHeightImage()):
                B, G, R = self.img[x][y]
                if (B == 0 and G == 255 and R == 0):
                    self.img[x, y] = (0, 0, 0)
        
        
    def setMaxSpacing(self, m):
        self.maxSpacing = self.getWidthImage()*m
        print(self.maxSpacing)
    
    def acceptedLumi(self, Y):
        #Y in [0, 255]
        if (Y > self.threshold + (255-self.threshold)*self.Lic):
            return True
        return False
    
    def acceptedGreen(self, H):
        #H in [0, 255]
        if (H >= 0.222222 and H <= 0.466667):
            return True
        return False
    
    def getClusterPoints(self):
        return self.clusterpoints
    
    def acceptedBlack(self, H):
        #Y in [0, 255]
        if (H < (40 + 40*self.Lic)):
            return True
        return False
     
    def getNewImage(self):
        return self.img
    
    def getOriginalImage(self):
        return self.img
    
    def getWidthImage(self):
        return self.width  
    
    def getHeightImage(self):
        return self.height
        
    def getLightIntensityScalar(self):
        return self.Lis
    
    def getSortedWhites(self):
        return self.white_list
  