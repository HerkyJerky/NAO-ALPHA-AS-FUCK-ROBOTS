import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import colorsys as cs
import ImageProcessing as ip

class Distance():
    
    def __init__(self, imgString): 
        #initialising the white points
        self.camHeight = 53 #in cm
        self.IP = ip.ImageProcessing(imgString)
        self.IP.setThreshold(170)
        self.IP.setMaxSpacing(0.05)
        self.IP.getAverageLightIntensity(self.IP.getWidthImage(), self.IP.getHeightImage(), self.IP.getOriginalImage(), 0.4)
        self.IP.startLumi()
        self.setClusterDensity(0.075)
        
        #generating a dummy image
        self.dummyImage()
        
                   
            
    def getDistance(self, A, B):
        #Euclidean distance
        D = (A[0] - B[0])*(A[0] - B[0]) + (A[1] - B[1])*(A[1] - B[1])
        return D
        
    def dummyImage(self):
        self.new_img = Image.new('RGB', (self.IP.getHeightImage(), self.IP.getWidthImage()), "black")
        pixels = self.new_img.load()
        w = self.getIP().getClusterPoints()
        
        for i in xrange(0, len(w)):
            pixels[w[i][0], w[i][1]] = (255, 255, 255)
            

    #cd in [0, 1] where cd is the fraction of the height of the image, make this value in [0.01, 0.1] preferably
    def setClusterDensity(self, cd):
        #width = height... image is kinda turned around
        self.clusterDistanceSquared = self.IP.getWidthImage()*cd*self.IP.getWidthImage()*cd
        
    def getIP(self):
        return self.IP


    def getNewImage(self):
        return self.new_img





#Test stuff

d = Distance('test2.png')   

 
img = d.getNewImage()
plt.title("Threshold = ")
plt.imshow(img)
plt.show()