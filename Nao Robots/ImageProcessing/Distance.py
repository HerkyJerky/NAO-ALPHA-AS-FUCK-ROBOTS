import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import colorsys as cs
import ImageProcessing as ip
from cv2 import cv

class Distance():
    
    def __init__(self, imgString): 
        
        self.camHeight = 53 #in cm
        self.IP = ip.ImageProcessing(imgString)
        self.IP.setThreshold(170)
        self.IP.setMaxSpacing(0.05)
        self.IP.getAverageLightIntensity(self.IP.getWidthImage(), self.IP.getHeightImage(), self.IP.getOriginalImage(), 0.4)
        self.IP.startLumi()
        
        self.findLandmarks()
        
    def findLandmarks(self):
        #edges = cv2.Canny(self.getIP().getNewImage(), 99, 100, apertureSize = 3)
        gray = cv2.cvtColor(self.getIP().getNewImage(),cv2.COLOR_BGR2GRAY)

        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray,2,3,0.04) 
        
        #result is dilated for marking the corners, not important
        dst = cv2.dilate(dst,None)

        # Threshold for an optimal value, it may vary depending on the image.
        self.getIP().getNewImage()[dst>0.01*dst.max()]=[0,0,255]
        
          
            
    def getDistance(self, A, B):
        #Euclidean distance
        D = (A[0] - B[0])*(A[0] - B[0]) + (A[1] - B[1])*(A[1] - B[1])
        return D       
        
    def getIP(self):
        return self.IP


    def getNewImage(self):
        return self.getIP().getOriginalImage()





#Test stuff

d = Distance('test2.png')   

 
img = d.getNewImage()
#plt.title("Threshold = ")
plt.imshow(img)
plt.show()