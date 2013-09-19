import sys
import time
import motions as mot
from naoqi import ALProxy

# KEEPER STATES
# BallFoundKeep()
# BallNotFoundKeep()
# BallApproaching()
# InGoalArea()

# PHASES
#The Keeper found the ball
def BallFoundKeep():
	global phase
	#Crouch towards the ball with legs close to each other
	#Follow ball
	print "BallFound!"	

#The Keeper doesn't see the ball
def BallNotFoundKeep():
	global phase
	#Look for the ball
	#phase='BallFoundKeep'
	print "BallNotFoundKeep!"

phases =     {
    'BallFoundKeep': BallFoundKeep,
    'BallNotFoundKeep': BallNotFoundKeep,
}

# END STATES

#Start Game
def start():
	global phase
	print "I'm a keeper!"
	phase = 'BallNotFoundKeep'
	phases.get(phase)()
