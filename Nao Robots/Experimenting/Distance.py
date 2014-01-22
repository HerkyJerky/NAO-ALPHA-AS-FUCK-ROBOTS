import cv2
#from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import colorsys as cs
from naoqi import ALProxy
import ImageProcessing as ip
import cv2.cv as cv
import math

#DEG2RAD = np.pi/180.0
##robotIp = "192.168.200.17"
#robotIp = "192.168.200.16"
#port = 9559
#memoryProxy =  ALProxy('ALMemory', robotIp, port)
#motionProxy = ALProxy("ALMotion", robotIp, port)
#RESW = 320.0 #320.0 #Capture width
#RESH = 240.0 #240.0 #Capture height
#CAMERA_H_FOV=46.4*DEG2RAD # Horizontal field of view
#CAMERA_V_FOV=34.8*DEG2RAD # Vertical field of view
#CAMERA_FOV_BEND_COEFFICIENT=pow(math.sin(CAMERA_H_FOV/2.0), 2) # X-Coefficient for circle segments within FOV

class Distance():


    def __init__(self, imgString, a, cameraHeight):

        self.min_slope = 0.3
        self.scalar = 0.001
        self.ang = a
        self.cameraHeight = cameraHeight

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

        gray = cv2.cvtColor(self.getIP().getImage(), cv2.COLOR_BGR2GRAY)
        self.edges = cv2.Canny(gray, 0, 100,  apertureSize=5)
        #self.edges = cv.Canny()
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

        self.fineTune(coordinates)


    def fineTune(self, coords):
        #print(coords)
        self.data = []

        #adding goalpost coordinates to the list
        gp = self.getIP().getGoalposts()
        if(len(gp) is not 0):
            for i in xrange(0, len(gp)):
                xgp, ygp = gp[i]
                da = self.calculateStuff(xgp, ygp, True)
                self.data.append(da)

        if(len(coords) is not 0):
            #removing the coordinates in lower 10% of image because of a lot of noise in that area
            tr = []
            for i in xrange(0, len(coords)):
                if(coords[i][1] > 0.9*self.IP.getWidthImage()):
                    tr.append(i)

            for i in xrange(0, len(tr)):
                coords.remove([coords[tr[len(tr)-1-i]][0], coords[tr[len(tr)-1-i]][1]])

            #for i in xrange(0, len(coords)):
                #self.getIP().getImage()[coords[i][1], coords[i][0]] = (0, 255, 0)

            #final part, getting actual distance:
            for i in xrange(0, len(coords)):
                da = self.calculateStuff(coords[i][0], coords[i][1], False)
                self.data.append(da)
                #print("coordinate white mark + distance(cm) + x-angle(rad):", coords[i], da)

    def getIP(self):
        return self.IP


    def calculateStuff(self, x, y, post):

        x2 = x
        y2 = y
        DEG2RAD = np.pi/180.0 # Convert Deg to Rad
        RAD2DEG = 180.0/np.pi # Convert Rad to Deg
        RESW = 320.0 #320.0 #Capture width
        RESH = 240.0 #240.0 #Capture height
        FOVHOR = 46.40 * DEG2RAD #"horizontal" field of view
        FOVVER = 34.80 * DEG2RAD #"vertical" field of view

        angle = self.ang * DEG2RAD
        B = angle - 0.5 * FOVVER # angle between ground to bottom of image
        HB = self.cameraHeight #height bot
        x = RESW - x # rotation counter clockwise
        x = x - RESW/2 # relative to center of image
        xAngle = (x/(RESW/2)) * (FOVHOR/2)  # in degrees
        y = RESH - y
        yAngle = B + (y/RESH) * FOVVER
        #print("yAngle", yAngle* RAD2DEG)
        distance = (HB * np.tan(yAngle)) / np.cos(xAngle)

        print (x2, y2)
        return (0.9*distance*100), xAngle, post

    #def calculateStuffTaghi(self,x,y,post):
    #    # TODO : test this method with actual NAO.
    #    # One thing : memory and motion and pitch and yaw should probably be instantiated somewhere else.
    #    pitch = memoryProxy.getData("Device/SubDeviceList/HeadPitch/Position/Actuator/Value")
    #    yaw = memoryProxy.getData("Device/SubDeviceList/HeadYaw/Position/Actuator/Value")
    #    ry=math.sqrt(pow((RESH-y)/float(RESH), 2)+pow((x/(RESW/2.0))-1.0, 2))
    #    alpha=ry*CAMERA_V_FOV  # angle within camera view
    #    beta=((math.pi/2.0) - (CAMERA_V_FOV/2)) - pitch  # angle of lower bound of camera view
    #    h = motionProxy.getTransform("CameraTop", 2, True)[11]
    #    dist=h*math.tan(alpha+beta)
    #    angle=-yaw+((x-(RESW/2.0))/RESW)*CAMERA_H_FOV  # calculate angle to object
    #    #ypos=-math.sin(angle)*dist  # calculate rel. y position
    #    #xpos=math.cos(angle)*dist  # calculate rel. x position
    #    print (x, y)
    #    return dist-1,angle,post

    def getData(self):
        return self.data
    
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
        if np.double(xA1 - xA2) == 0:
            slopeA = 9001
        else:
            slopeA = (np.double(yA1 - yA2)/np.double(xA1 - xA2))
        if np.double(xB1 - xB2) == 0:
            slopeB = 9001
        else:
            slopeB = (np.double(yB1 - yB2)/np.double(xB1 - xB2))
        if(np.abs(slopeA - slopeB) < self.min_slope):
            return True
        return False


    def getNewImage(self):
        #return self.edges
        return self.getIP().getImage()


#Test stuff
#d = Distance('9jan03-7.png')   
#img = d.getNewImage()
#print(d.getData())
#plt.title("Threshold = ")
#plt.imshow(img)
#plt.show()
