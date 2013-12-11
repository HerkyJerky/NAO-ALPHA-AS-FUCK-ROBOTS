__author__ = 'redsphinx'

import time
from naoqi import ALProxy
import Image
from Logger import Logger
import math
import vision_definitions
import numpy as np

robotIp = "192.168.200.16"
port = 9559
#global visionProxy
#resolution = 2    # VGA
resolution = vision_definitions.kQQVGA  # QQVGA (160 * 120)
#colorSpace = 11   # RGB
#colorSpace = vision_definitions. nt sure whats happening here
logObj = Logger()
DEG2RAD = math.pi/180.0 # Convert Deg to Rad
RAD2DEG = 180.0/math.pi # Convert Rad to Deg
CAMERA_H_FOV = 46.4 * DEG2RAD # Horizontal field of view
CAMERA_V_FOV = 34.8 * DEG2RAD # Vertical field of view
RESW = 160.0 #Capture width
RESH = 120.0 #Capture height
FOVHOR = 46.40 #"horizontal" field of view
FOVVER = 34.80 #"vertical" field of view

class Vision:
    def __init__(self):
        self.visionProxy = ALProxy("ALVideoDevice", robotIp, port)
        pass

    def takePic(self, name):
        videoClient = self.visionProxy.subscribe("python_client", resolution, colorSpace, 5)
        picture = self.visionProxy.getImageRemote(videoClient)
        self.visionProxy.unsubscribe(videoClient)
        picWidth = picture[0]
        picHeight = picture[1]
        array = picture[6]
        realPicture = Image.fromstring("RGB", (picWidth, picHeight), array)
        realPicture.save(name, "PNG")
        realPicture.show()
        logObj.logWrite(time.time().__str__() + "_5_{0}_0_0_0".format(name))
        pass

    def analyze(self):
        # TODO: Roel fill in your beautiful code.
        logObj.logWrite(time.time().__str__() + "_6_0_0_0_0")
        pass

    def getDistanceFromLandMark(self, x, y): # returns x Angle and the distance from the landmark in cm

        B = 45 - 0.5 * FOVVER # angle between ground to bottom of image
        HB = 53 # height of camera
        x = RESW - x # rotation counter clockwise
        x = x - RESW/2 # relative to center of image
        xAngle = x/(RESW/2) * FOVHOR/2 # in degrees
        y = RESH - y
        yAngle = B + y/RESH * FOVVER
        yAngle = yAngle * DEG2RAD
        xAngle = xAngle * DEG2RAD
        distance = HB * np.tan(yAngle)
        distance = distance / np.cos(xAngle)

        return xAngle, distance
        pass


#vis = Vision()
##vis.takePic("selfie2")
#print(vis.getDistanceFromLandMark(35, 100))
