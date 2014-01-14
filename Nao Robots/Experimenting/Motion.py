__author__ = 'redsphinx'

import time
from naoqi import ALProxy
from Logger import Logger
import math
import re

robotIp = "192.168.200.17"
port = 9559
logObj = Logger()
MAXSTEPSIZE = 0.08  # in meters
MINSTEPSIZE = 0.04  # in meters
MAXTHETA = 30  # in degrees CHANGED TO RADIANS IN CALCULATIONS
MINTHETA = 10  # same
UNIT = 0.04  # the unit of distance in our case. so the robot moves in multiplicities of this unit
THETAUNIT = 10
RLEG = "RLeg"
LLEG = "LLeg"
SPEED = 0.4  # decrease to increase accuracy, robot will move slower though
DIRECTIONS = ["L", "R", "Fw", "Bw"]
DEG2RAD = math.pi/180.0 # Convert Deg to Rad
RAD2DEG = 180.0/math.pi # Convert Rad to Deg

class Motion:
    def __init__(self):
        self.motionProxy = ALProxy("ALMotion", robotIp, port)
        self.postureProxy = ALProxy("ALRobotPosture", robotIp, port)
        self.talkProxy = ALProxy("ALTextToSpeech", robotIp, port)
        robotConfig = self.motionProxy.getRobotConfig()
        for i in range(len(robotConfig[0])):
            print robotConfig[0][i], ": ", robotConfig[1][i]

    # turn on stiffness of body
    # harden
    def stiffnessOn(self, motionProxy):
        allJoints = "Body"
        pStiffnessLists = 1.0
        pTimeLists = 1.0
        motionProxy.stiffnessInterpolation(allJoints, pStiffnessLists, pTimeLists)

    # turn off stiffness
    def stiffnessOff(self, motionProxy):
        allJoints = "Body"
        pStiffnessLists = 0.0
        pTimeLists = 1.0
        motionProxy.stiffnessInterpolation(allJoints, pStiffnessLists, pTimeLists)

    # when standing, stand up straight by setting all angles in the body to default
    #def standStraight(self):
    #    names = 'Body'
    #    angles = 0.1
    #    fractionMaxSpeed = 0.1
    #    self.motionProxy.setAngles(names, angles, fractionMaxSpeed)
    #    # TODO if this doesn't work then do all relevant joints 1 by 1


    # make robot stand up
    def stand(self):  # def stand(self, name, speed):
        self.stiffnessOn(motionProxy=self.motionProxy)
        self.postureProxy.goToPosture("Stand", 1.0)
        #motionProxy.setWalkArmsEnabled(True, True)
        #motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
        #logObj.logWrite(time.time().__str__() + "_1_0_0_0_0")

    # make the robot sit
    def sit(self):
        self.stiffnessOn(motionProxy=self.motionProxy)
        self.postureProxy.goToPosture("SitRelax", 1.0)
        #logObj.logWrite(time.time().__str__() + "_2_0_0_0_0")

    '''
    make the robot move in a direction
    x: positive move forward, negative move backwards [-1.0 to 1.0]
    y: positive left, negative right [-1.0 to 1.0]
    theta: positive for counterclockwise, negative for clockwise [-1.0 to 1.0]
    speed: determines the frequency of the steps, so the velocity [0.0 to 1.0]
    '''
    def move(self, x, y, theta, speed):
        x = float(x)
        y = float(y)
        theta = float(theta)
        speed = float(speed)
        self.motionProxy.setWalkTargetVelocity(x, y, theta, speed)
        logObj.logWrite(time.time().__str__() + "_3_{0}_{1}_{2}_{3}".format(x,y,theta,speed))

    '''
    as an alternative and more controllable method of moving,
    this moves the robot a desired amount of m in units of 0.05. This method makes the robot move L R Fw Bw
    for rotation see the rotateTheta() method
    DIRECTIONS = ["L", "R", "Fw", "Bw"]
    sends as output [time,action,dForwards,dSideways,dtheta,speed]

    Action code = 1
    '''
    # TODO figure out how many m one footstep is, for all cases so L R Bw Fw
    def moveXYCm(self, x, y):
        x = float(re.match(r'\d+',x).group())
        y = float(re.match(r'\d+',y).group())
        print(x, y)
        print(x + 2 + y)
        print(x%0.04)
        action = 1
        theta = 0
        #self.standStraight()
        self.motionProxy.walkInit()

        # pos is L, neg is R
        if x == 0:
            amountStepsY = int(self.getSteps(y)[0])
            stepSizeY = int(self.getSteps(y)[1])
            amountStepsX = 0
            stepSizeX = 0
            if y > 0:
                positivity = True
                direction = DIRECTIONS[0]
                stepSize = stepSizeY
                for i in xrange(0, amountStepsY):
                    if i % 2 == 0:
                        self.setStep(LLEG, stepSizeX, stepSizeY, theta)

                        lastMovedLeg = LLEG
                    else:
                        self.setStep(RLEG, stepSizeX, stepSizeY, theta)
                        lastMovedLeg = RLEG
            else:
                positivity = False
                direction = DIRECTIONS[1]
                stepSize = -stepSizeY
                for i in xrange(0, amountStepsY):
                    if i % 2 == 0:
                        self.setStep(RLEG, -stepSizeX, -stepSizeY, theta)
                        lastMovedLeg = RLEG
                    else:
                        self.setStep(LLEG, -stepSizeX, -stepSizeY, theta)
                        lastMovedLeg = LLEG
            self.setLastStep(lastMovedLeg, direction, positivity, stepSize)

        # pos is Fw, neg is Bw
        elif y == 0:
            amountStepsX = self.getSteps(x)[0], stepSizeX = self.getSteps(x)[1]
            amountStepsY, stepSizeY = 0
            if x > 0:
                positivity = True
                direction = DIRECTIONS[2]
                stepSize = stepSizeX
                for i in xrange(0, amountStepsX):
                    if i % 2 == 0:
                        self.setStep(RLEG, stepSizeX, stepSizeY, theta)
                        lastMovedLeg = RLEG
                    else:
                        self.setStep(LLEG, stepSizeX, stepSizeY, theta)
                        lastMovedLeg = LLEG
            else:
                positivity = False
                direction = DIRECTIONS[3]
                stepSize = -stepSizeX
                for i in xrange(0, amountStepsY):
                    if i % 2 == 0:
                        self.setStep(RLEG, -stepSizeX, -stepSizeY, theta)
                        lastMovedLeg = RLEG
                    else:
                        self.setStep(LLEG, -stepSizeX, -stepSizeY, theta)
                        lastMovedLeg = LLEG
            self.setLastStep(lastMovedLeg, direction, positivity, stepSize)
        else:
            print "error: either x or y input has to be 0"

        #self.standStraight()
        logObj.logWrite(time.time().__str__() + "_{0}_{1}_{2}_{3}_{4}".format(action, x, y, theta, SPEED))
        return [time.time().__str__(), action, x, y, theta, SPEED]
        pass

    # returns how many steps to take and with which step size
    def getSteps(self, distance):
        distance = math.fabs(distance)
        if distance % MAXSTEPSIZE == 0:
            steps = distance/(UNIT*(MAXSTEPSIZE/MINSTEPSIZE))
            stepSize = MAXSTEPSIZE
        elif distance % MINSTEPSIZE == 0:
            steps = distance/UNIT
            stepSize = MINSTEPSIZE
        else:
            steps = 0
            stepSize = 0
            print("distance is not valid; must be a multiplication of ", UNIT)
        return [steps, stepSize]

    # set a step with a speed
    def setStep(self, legName, X, Y, Theta):
        footSteps = [[X, Y, Theta]]
        fractionMaxSpeed = [SPEED]
        clearExisting = False
        self.motionProxy.setFootStepsWithSpeed(legName, footSteps, fractionMaxSpeed, clearExisting)

    # set the last step to complete the movement
    # DIRECTIONS = ["L", "R", "Fw", "Bw"]
    def setLastStep(self, lastMovedLeg, direction, positivity, stepSize):
        theta = 0
        if lastMovedLeg == LLEG:
            legToMove = RLEG
        elif lastMovedLeg == RLEG:
            legToMove = LLEG
        if direction == (DIRECTIONS[0], DIRECTIONS[1]):
            x = 0
            y = 0 # TODO something with stepSize? no idea, since this moves the foot a distance relative to the other foot
        elif direction == (DIRECTIONS[2], DIRECTIONS[3]):
            x = 0 # TODO something with stepSize? see TODO above
            y = 0
        self.setStep(legToMove, x, y, theta)
        #self.standStraight()

    # get the amount of steps needed to rotate amount of theta in. steps is how many steps the NAO needs to take to make the turn,
    # thetaSize is the size of theta in degrees of a turn in one step
    def getThetaSteps(self, theta):
        theta = math.fabs(theta)
        if theta % MAXTHETA == 0:
            steps = theta/(THETAUNIT*(MAXTHETA/MINTHETA))
            thetaSize = MAXTHETA
        elif theta % MINTHETA == 0:
            steps = theta/THETAUNIT
            thetaSize = MINTHETA
        else:
            steps = 0
            print("theta is not valid; must be a multiplication of " + MINTHETA)
        return steps, thetaSize

    # rotate an n amount of theta in degrees.
    # one turn step = 29.9656927 deg or 0.523 radians
    # theta: positive for counterclockwise, negative for clockwise [-1.0 to 1.0]
    # action code = 2
    def rotateTheta(self, theta):
        action = 2
        x = 0
        y = 0
        steps, thetaSize = self.getThetaSteps(theta)
        if theta < 0:
            startLeg = RLEG
            otherLeg = LLEG
            thetaSize = -thetaSize*DEG2RAD
        else:
            startLeg = LLEG
            otherLeg = RLEG
            thetaSize = thetaSize*DEG2RAD

        #self.standStraight()
        self.motionProxy.walkInit()
        footSteps = [[0, 0, thetaSize]]
        fractionMaxSpeed = [SPEED]
        clearExisting = False

        for i in xrange(0, steps):
            if i % 2 == 0:
                self.motionProxy.setFootStepsWithSpeed(startLeg, footSteps, fractionMaxSpeed, clearExisting)
            else:
                self.motionProxy.setFootStepsWithSpeed(otherLeg, footSteps, fractionMaxSpeed, clearExisting)

        # TODO take last step?
        #self.standStraight()
        logObj.logWrite(time.time().__str__() + "_{0}_{1}_{2}_{3}_{4}".format(action, x, y, theta*DEG2RAD, SPEED))
        return [time.time().__str__(), action, x, y, theta*DEG2RAD, SPEED]


    # stop the walking gracefully
    def stop(self):
        #self.motionProxy.stopMove()
        self.motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.0)
        #logObj.logWrite(time.time().__str__() + "_4_0_0_0_0")

    def talk(self, word):
        self.talkProxy.say(word)
        #logObj.logWrite(time.time().__str__() + "_8_{0}_0_0_0".format(word))

    # head pitch: 81.15 degrees
    def moveHeadPitch(self, theta, speed):
        theta = float(theta)
        speed = float(speed)
        self.motionProxy.setAngles("HeadPitch", theta, speed)
        #logObj.logWrite(time.time().__str__() + "_9_{0}_{1}_0_0".format(theta, speed))

    def lieDownRelax(self):
        self.stiffnessOn(motionProxy=self.motionProxy)
        self.postureProxy.goToPosture("LyingBack", 1.0)
        self.stiffnessOff(motionProxy=self.motionProxy)
        #logObj.logWrite(time.time().__str__() + "_10_0_0_0_0")

#mot = Motion()
##mot.stand()
##mot.sit()
#
#mot.standStraight()