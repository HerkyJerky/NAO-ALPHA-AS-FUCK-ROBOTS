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
        self.IP.getAverageLightIntensity(self.IP.getWidthImage(), self.IP.getHeightImage(), self.IP.getImage(), 0.4)
        self.IP.startLumi()
        avgSizeImage = ((self.getIP().getHeightImage() + self.getIP().getWidthImage())/2)*0.075
        self.minDistanceSquared = avgSizeImage*avgSizeImage
        
        self.findLandmarks()
        
        
    def findLandmarks(self):
        #self.edges = cv2.Canny(self.getIP().getNewImage(), 0, 100, apertureSize = 3)
        #gray = cv2.cvtColor(self.getIP().getNewImage(),cv2.COLOR_BGR2GRAY)
        #gray = np.float32(gray)
        coordinates = []
        
        #dst = cv2.cornerHarris(gray,3,13,0.1) 
        
        #result is dilated for marking the corners, not important
        #dst = cv2.dilate(dst,None)

        # Threshold for an optimal value, it may vary depending on the image.
        #self.getIP().getNewImage()[dst>0.01*dst.max()]=[0,0,255]
        
        self.edges = cv2.cvtColor(self.getIP().getImage(),cv2.COLOR_BGR2GRAY)
        lines = cv2.HoughLinesP(self.edges,1,np.pi/360, 15, minLineLength = 20, maxLineGap = 10)
        if len(lines) is not 0:
            for i in xrange(0, len(lines[0])):
                xA1,yA1,xA2,yA2 = lines[0][i]
                for j in xrange(i+1, len(lines[0])):
                    xB1,yB1,xB2,yB2 = lines[0][j]
                    #cv2.line(self.edges,(x1,y1),(x2,y2),(255,255,255),2)
                    close = self.closeEnough(xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2)
                    if(not self.straightLine(xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2) 
                       and close[0]):
                        if (len(coordinates) is not 0):
                            double = False
                            for k in xrange(0, len(coordinates)):
                                if((close[1] - coordinates[k][0])*(close[1] - coordinates[k][0]) 
                                   + (close[2] - coordinates[k][1])*(close[2] - coordinates[k][1]) < self.minDistanceSquared):
                                    double = True
                            if(double is False):
                                coordinates.append([close[1], close[2]])
                                self.getIP().getImage()[close[2], close[1]] = (0, 255, 0)
                        else:    
                            coordinates.append([close[1], close[2]])
                            self.getIP().getImage()[close[2], close[1]] = (0, 255, 0)
        print(coordinates)              
    
    
    def getIP(self):
        return self.IP
    
    
    def closeEnough(self, xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2):
        if (((xA1 - xB1)*(xA1 - xB1) + (yA1 - yB1)*(yA1 - yB1)) <= self.minDistanceSquared):
            return True, xA1, yA1
        elif (((xA1 - xB2)*(xA1 - xB2) + (yA1 - yB2)*(yA1 - yB2)) <= self.minDistanceSquared):
            return True, xA1, yA1, xB2, yB2
        elif (((xA2 - xB1)*(xA2 - xB1) + (yA2 - yB1)*(yA2 - yB1)) <= self.minDistanceSquared):
            return True, xA2, yA2
        elif (((xA2 - xB2)*(xA2 - xB2) + (yA2 - yB2)*(yA2 - yB2)) <= self.minDistanceSquared):
            return True, xA2, yA2
        return False, 0, 0
    
    
    def straightLine(self, xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2):
        slopeA = (np.double(yA1 - yA2)/np.double(xA1 - xA2))
        slopeB = (np.double(yB1 - yB2)/np.double(xB1 - xB2))
        if(np.abs(slopeA - slopeB) > 0.2):
            return False
        return True


    def getNewImage(self):
        #return self.edges
        return self.getIP().getImage()


#Test stuff
d = Distance('test2.png')   
 
img = d.getNewImage()
#plt.title("Threshold = ")
plt.imshow(img)
plt.show()