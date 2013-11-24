__author__ = 'redsphinx'

import time
from naoqi import ALProxy
import Image
from Logger import Logger

robotIp = "192.168.200.16"
port = 9559
#global visionProxy
resolution = 2    # VGA
colorSpace = 11   # RGB
logObj = Logger()

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

#vis = Vision()
#vis.takePic("selfie2")