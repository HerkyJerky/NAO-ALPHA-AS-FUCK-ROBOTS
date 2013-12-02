__author__ = 'redsphinx'

import time
from naoqi import ALProxy
import Image
from Logger import Logger
import math

robotIp = "192.168.200.16"
port = 9559
#global visionProxy
resolution = 2    # VGA
colorSpace = 11   # RGB
logObj = Logger()


# some constants that are maybe needed
DEG2RAD = math.pi/180.0 # Convert Deg to Rad
RAD2DEG = 180.0/math.pi # Convert Rad to Deg
CAMERA_H_FOV=46.4*DEG2RAD # Horizontal field of view
CAMERA_V_FOV=34.8*DEG2RAD # Vertical field of view
CAMERA_FOV_BEND_COEFFICIENT=math.pow(math.sin(CAMERA_H_FOV/2.0), 2) # X-Coefficient for circle segments within FOV
BALL_DIAM = 0.087
RESW=640 #Capture width
RESH=480 #Capture height

class Vision:
    def __init__(self):
        self.visionProxy = ALProxy("ALVideoDevice", robotIp, port)
        pass

    def takePic(self, name):
        print("picture being taken...")
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

    def getDistanceFromLandMark(self, x, y):

        pass




def getCoordinates(image, yaw, pitch):
    x, y, w = processImage(image)
    ry=math.sqrt(math.pow((RESH-y)/RESH, 2)+CAMERA_FOV_BEND_COEFFICIENT*math.pow((x/(RESW/2.0))-1.0, 2))
    alpha=ry*CAMERA_V_FOV  # angle within camera view
    beta=((math.pi/2.0) - (CAMERA_V_FOV/2.0)) - pitch[0]  # angle of lower bound of camera view
    h = motion.getPosition("CameraTop", 2, True)
    dist=h[2]*math.tan(alpha+beta)
    angle=-yaw[0]+((x-(RESW/2.0))/RESW)*CAMERA_H_FOV  # calculate angle to object
    ypos=-math.sin(angle)*dist  # calculate rel. y position
    xpos=math.cos(angle)*dist  # calculate rel. x position
    return xpos, ypos, angle

#vis = Vision()
#vis.takePic("selfie2")