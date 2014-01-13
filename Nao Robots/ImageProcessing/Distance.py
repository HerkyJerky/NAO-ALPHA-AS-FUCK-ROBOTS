import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import colorsys as cs
import ImageProcessing as ip
from cv2 import cv

class Distance():
    
    
    def __init__(self, imgString): 
        
        self.min_slope = 0.3
        self.scalar = 0.001
        
        self.IP = ip.ImageProcessing(imgString)
        self.IP.setThreshold(120)
        self.IP.getAverageLightIntensity(self.IP.getWidthImage(), self.IP.getHeightImage(), self.IP.getImage(), 0.4)
        self.IP.startLumi()
        avgSizeImage = ((self.getIP().getHeightImage() + self.getIP().getWidthImage())/2)
        self.minDistanceSquared = avgSizeImage*avgSizeImage*self.scalar
        self.minDistanceSquared2 = self.minDistanceSquared*5
        #print("min distance:", np.sqrt(self.minDistanceSquared))
        self.findLandmarks()
        
        
    def findLandmarks(self):
        self.edges = cv2.Canny(self.getIP().getImage(), 0, 100, apertureSize = 5)
        #gray = cv2.cvtColor(self.getIP().getNewImage(),cv2.COLOR_BGR2GRAY)
        #gray = np.float32(gray)
        coordinates = []
        
        #dst = cv2.cornerHarris(gray,3,13,0.1) 
        
        #result is dilated for marking the corners, not important
        #dst = cv2.dilate(dst,None)

        # Threshold for an optimal value, it may vary depending on the image.
        #self.getIP().getNewImage()[dst>0.01*dst.max()]=[0,0,255]
        
        #self.edges = cv2.cvtColor(self.getIP().getImage(),cv2.COLOR_BGR2GRAY)
        lines = []
        lines = cv2.HoughLinesP(self.edges,1,np.pi/360, 10, minLineLength = 40, maxLineGap = 5)
        if lines is not None:
            for i in xrange(0, len(lines[0])):
                xA1,yA1,xA2,yA2 = lines[0][i]
                cv2.line(self.edges,(xA1,yA1),(xA2,yA2),(255,255,255),2)
                #print(lines[0][i])
                for j in xrange(i+1, len(lines[0])):
                    xB1,yB1,xB2,yB2 = lines[0][j]
                    close = self.closeEnough(xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2)
                    straight = self.straightLine(xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2)
                    if(close[0] and not straight):
                        #print(close[1], close[2])
                        if (len(coordinates) is not 0):
                            double = False
                            for k in xrange(0, len(coordinates)):
                                yScalar = ((close[2] + coordinates[k][1])/(2.0*240.0)) + 1.0
                                if((close[1] - coordinates[k][0])*(close[1] - coordinates[k][0]) 
                                   + (close[2] - coordinates[k][1])*(close[2] - coordinates[k][1]) < self.minDistanceSquared2*yScalar):
                                    double = True
                            if(double is False):
                                coordinates.append([close[1], close[2]])
                                #self.getIP().getImage()[close[2], close[1]] = (0, 255, 0)
                        else:    
                            coordinates.append([close[1], close[2]])
                            #self.getIP().getImage()[close[2], close[1]] = (0, 255, 0)
                            
                            
        if len(coordinates) is not 0:    
            self.fineTune(coordinates)
        
    def fineTune(self, coords):
        #print(coords)
        
        #removing the coordinates in lower 10% of image because of a lot of noise in that area
        tr = []
        for i in xrange(0, len(coords)):
            if(coords[i][1] > 0.9*self.IP.getWidthImage()):
                tr.append(i)
        for i in xrange(0, len(tr)):
            coords.remove([coords[tr[len(tr)-1-i]][0], coords[tr[len(tr)-1-i]][1]])        
        
        for i in xrange(0, len(coords)):
            self.getIP().getImage()[coords[i][1], coords[i][0]] = (0, 255, 0)
        
        #final part, getting actual distance:
        for i in xrange(0, len(coords)):
            da = self.calculateStuff(coords[i][0], coords[i][1])
            print("coordinate white mark + distance(cm) + x-angle(rad):", coords[i], da)
        
    
    def getIP(self):
        return self.IP
    

    def calculateStuff(self, x, y):
        
        DEG2RAD = np.pi/180.0 # Convert Deg to Rad
        RAD2DEG = 180.0/np.pi # Convert Rad to Deg
        RESW = 320.0 #320.0 #Capture width
        RESH = 240.0 #240.0 #Capture height
        FOVHOR = 46.40 * DEG2RAD #"horizontal" field of view
        FOVVER = 34.80 * DEG2RAD #"vertical" field of view
        
        angle = 71.8 * DEG2RAD
        B = angle - 0.5 * FOVVER # angle between ground to bottom of image
        HB = 53.0 # height of camera
        x = RESW - x # rotation counter clockwise
        x = x - RESW/2 # relative to center of image
        xAngle = (x/(RESW/2)) * (FOVHOR/2) # in degrees
        y = RESH - y
        yAngle = B + (y/RESH) * FOVVER
        #print("yAngle", yAngle* RAD2DEG)
        distance = (HB * np.tan(yAngle)) / np.cos(xAngle)

        return distance, xAngle
    
    
    def closeEnough(self, xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2):
        
        yScalar = 1 - ((yA1 + yB1)/(2.0*240.0)) + 1.0
        if (((xA1 - xB1)*(xA1 - xB1) + (yA1 - yB1)*(yA1 - yB1)) <= (self.minDistanceSquared/yScalar)):
            return True, xA1, yA1
        
        yScalar = ((yA1 + yB2)/(2.0*240.0)) + 1.0
        if (((xA1 - xB2)*(xA1 - xB2) + (yA1 - yB2)*(yA1 - yB2)) <= (self.minDistanceSquared/yScalar)):
            return True, xA1, yA1
        
        yScalar = ((yA2 + yB1)/(2.0*240.0)) + 1.0
        if (((xA2 - xB1)*(xA2 - xB1) + (yA2 - yB1)*(yA2 - yB1)) <= (self.minDistanceSquared/yScalar)):
            return True, xA2, yA2
        
        yScalar = ((yA2 + yB2)/(2.0*240.0)) + 1.0
        if (((xA2 - xB2)*(xA2 - xB2) + (yA2 - yB2)*(yA2 - yB2)) <= (self.minDistanceSquared/yScalar)):
            return True, xA2, yA2
        return False, 0, 0
    
    
    def straightLine(self, xA1, xA2, yA1, yA2, xB1, xB2, yB1, yB2):
        slopeA = (np.double(yA1 - yA2)/np.double(xA1 - xA2))
        slopeB = (np.double(yB1 - yB2)/np.double(xB1 - xB2))
        #print(np.abs(slopeA - slopeB))
        if(np.abs(slopeA - slopeB) < self.min_slope):
            return True
        return False


    def getNewImage(self):
        return self.edges
        #return self.getIP().getImage()


#Test stuff
d = Distance('9jan03-7.png')   
img = d.getNewImage()
#plt.title("Threshold = ")
plt.imshow(img)
plt.show()