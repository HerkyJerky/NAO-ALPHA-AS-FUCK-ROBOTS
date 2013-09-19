
import sys
import time
import threading
import math
import statecontroller as sc
import motions as mot
import player
import keeper

from naoqi import ALProxy
import settings

#Get connection settings
IP = settings.getIP()
PORT = settings.getPort()

#Get state
state = sc.getState()
phase = 'BallNotFound'
#Get Tuype
playerType = sc.getRobotNumber()

playerTypes = {
	0: player,
	1: keeper
}

print "Connecting to", IP, "with port", PORT

pose = ALProxy('ALRobotPose', IP, PORT)
posture = ALProxy('ALRobotPosture', IP, PORT)

# STATES

#walk to the starting position
#GOES TO: setstate
def Ready():
	posture.goToPosture('StandInit', 0.5)

#wait for the kickoff
#GOES TO: playing
def Set():
	posture.goToPosture('StandInit', 0.5)

#look for the ball, try to kick it. Or if youre a goalkeeper, stay put
#if chest is pressed go to penalized
#GOES TO:finished,ready,penalized
def Playing():
	if mot.checkStandUp():
		playerTypes.get(playerType).start()
	else:
		playerTypes.get(playerType).resume()
	

#stand up, if left bumper is pressed switch colour, press chest to go to penalized
#GOES TO: ready, penalized
def Initial():
	posture.goToPosture('StandInit', 0.5)

#Done, do nothing
def Finished():
	if mot.isWalking():
		mot.killWalk()
	posture.goToPosture('StandInit', 0.5)

states =     {
    0: Initial,
    1: Ready,
    2: Set,
    3: Playing,
    4: Finished
}

# END STATES

# Constant updating the state
class stateUpdate(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global state
        while(1):
            state = sc.getState()
        print 'stopped'

update = stateUpdate("stateUpdate")

#Begins the game
def awakeMind():
	global state
	# sc.start()
	update.start()
	mot.stiff()
	while(1):
		print "State: ", state
		states.get(state)()
	
awakeMind()
