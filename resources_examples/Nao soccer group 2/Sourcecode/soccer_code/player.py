import sys
import time
import math
import motions as mot
import vision as vis
from naoqi import ALProxy
import settings

#Player starts in ball not found state
phase = 'BallNotFound'

# PLAYER FUNCTIONS

#Scan the field for the ball with predifined angles for the head so you don't have overlap
def scanCircle():            
    #Check to stop the head from making unnecessary movements
    print 'Scanning Circle'
    #Try to find ball
    ball = vis.findBall()
    if ball != (0,0,0,0):
        return ball
    #Predifined angles
    for angles in [(-1.1, -0.4), (-0.5, -0.4), (-0.25, -0.4), ( 0, -0.4),(0.25, -0.4), ( 0.5, -0.4), ( 1.1, -0.4), \
                   ( 1,  0.1  ), (0.75, 0.1), ( 0.5,  0.1  ), (0.25, 0.1), ( 0,  0.1  ), (-0.25, 0.1), (-0.5,  0.1  ), (-0.75, 0.1), (-1,  0.1  ), \
                   (-1,  0.4), (-0.5,  0.4),  ( 0,  0.5),  ( 0.5,  0.4),( 1,  0.4), (0,0) ]: 
                   # last one is to make successive scans easier
        #Set head angles
        mot.setHeadBlock((angles[0], angles[1], 0.2))
        #Try to find ball
        ball = vis.findBall()
        #Return ball when found
        if ball != (0,0,0,0):
            return ball
# END PLAYER FUNCTIONS


# PLAYER PHASES
# BallFound()
# BallNotFound()
# Kick()
# Unpenalized()
# ReturnField()

#Phase BallFound
def BallFound():
	global phase
	print "Phase: BallFound"
	#Try to find ball
	ball = vis.findBall()
	if ball != (0,0,0,0):
		#If you found a ball assign x,y, Xangle,Yangle
		(x,y,z,p) = ball
		#If it is close enough
		#if x < 0.225 and -0.02 < y < 0.02: # x was 0.225
		print 'Kick'
		#Stop walking
		mot.killWalk()
		#Find the Goal and position correctly

		#New Phase Kick
		phase = 'Kick'
		return True
		#If it's to far walk towards it
		if x > 0.375 or y > 0.25 or y < -0.25:
	            x = x * 2.5
	            y = y * 1.5
	            if x > 1:
	                x = 1
	            if y > 1:
	                y = 1
	            if y < -1:
	                y = -1
	            f = 1.0
	        else:
	            f = 0.9
	        if x >= -1:
	        	#Walk with specified velocity to the target
	            mot.SWTV(x-0.15,y,math.atan(y/x)/2.5, f) 
	            print 'Is Walking'
	else:
		print ball
		mot.killWalk()
		phase = 'BallNotFound'

#Ball Not found phase
def BallNotFound():
	global phase
	print "Phase: BallNotFound"
	#Try to find a ball
	if scanCircle():
		phase = 'BallFound'
	#If no ball is found
	else:
		#Circle slowly
		mot.postWalkTo((0, 0, 1.3))		
		print 'Turning'

#Kicking phase
def Kick():
	global phase
        mot.setHeadBlock((0,-0.5, 0.2))
	vis.findGoal()
	print "Phase: Kick"
	mot.newKick()
	#mot.rKickAngled(0.2)
	phase = 'BallNotFound'


phases =     {
    'BallFound': BallFound,
    'BallNotFound': BallNotFound,
    'Kick' : Kick,
}

# END FACES
#Start Game
def start():
	global phase
	print "Starting..."
	phase = 'BallNotFound'
	phases.get(phase)()
	
#Resume when paused
def resume():
	global phase
	print 'Resuming...'
	phases.get(phase)()


