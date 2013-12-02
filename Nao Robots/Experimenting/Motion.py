__author__ = 'redsphinx'

import time
from naoqi import ALProxy
from Logger import Logger

robotIp = "192.168.200.16"
port = 9559
logObj = Logger()


class Motion:
    def __init__(self):
        self.motionProxy = ALProxy("ALMotion", robotIp, port)
        self.postureProxy = ALProxy("ALRobotPosture", robotIp, port)
        self.talkProxy = ALProxy("ALTextToSpeech", robotIp, port)
        pass

    # turn on stiffness of body
    # harden
    def stiffnessOn(self, motionProxy):
        allJoints = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        motionProxy.stiffnessInterpolation(allJoints, pStiffnessLists, pTimeLists)
        pass

    def stiffnessOff(self, motionProxy):
        allJoints = "Body"
        pStiffnessLists = 0.0
        pTimeLists = 1.0
        motionProxy.stiffnessInterpolation(allJoints, pStiffnessLists, pTimeLists)
        pass

    # make robot stand up
    def stand(self):  # def stand(self, name, speed):
        self.stiffnessOn(motionProxy=self.motionProxy)
        self.postureProxy.goToPosture("Stand", 1.0)
        #motionProxy.setWalkArmsEnabled(True, True)
        #motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        logObj.logWrite(time.time().__str__() + "_1_0_0_0_0")
        pass

    # make the robot sit
    def sit(self):
        self.stiffnessOn(motionProxy=self.motionProxy)
        self.postureProxy.goToPosture("SitRelax", 1.0)
        logObj.logWrite(time.time().__str__() + "_2_0_0_0_0")
        pass

    # make the robot move in a direction
    # x: positive move forward, negative move backwards [-1.0 to 1.0]
    # y: positive left, negative right [-1.0 to 1.0]
    # theta: positive for counterclockwise, negative for clockwise [-1.0 to 1.0]
    # speed: determines the frequency of the steps, so the velocity [0.0 to 1.0]
    def move(self, x, y, theta, speed):
        x = float(x)
        y = float(y)
        theta = float(theta)
        speed = float(speed)
        self.motionProxy.setWalkTargetVelocity(x, y, theta, speed)
        logObj.logWrite(time.time().__str__() + "_3_{0}_{1}_{2}_{3}".format(x,y,theta,speed))
        pass

    def stop(self):
        self.motionProxy.stopMove()
        logObj.logWrite(time.time().__str__() + "_4_0_0_0_0")
        pass

    def talk(self, word):
        self.talkProxy.say(word)
        logObj.logWrite(time.time().__str__() + "_8_{0}_0_0_0".format(word))
        pass

    def moveHeadPitch(self, theta, speed):
        theta = float(theta)
        speed = float(speed)
        self.motionProxy.setAngles("HeadPitch", theta, speed)
        logObj.logWrite(time.time().__str__() + "_9_{0}_{1}_0_0".format(theta, speed))
        pass

    def lieDownRelax(self):
        self.stiffnessOn(motionProxy=self.motionProxy)
        self.postureProxy.goToPosture("LyingBack", 1.0)
        self.stiffnessOff(motionProxy=self.motionProxy)
        logObj.logWrite(time.time().__str__() + "_10_0_0_0_0")
        pass

#mot = Motion()
#mot.stand()
#mot.sit()
