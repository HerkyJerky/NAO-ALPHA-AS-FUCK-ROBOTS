import cv
import cv2
import sys
import Image
import time
from math import *
from naoqi import ALProxy
import numpy as np  
import settings

IP = settings.getIP()
PORT = settings.getPort()

global h, s, v, i, im
posx = 0
posy = 0
motion = ALProxy("ALMotion", IP, PORT)
camProxy = ALProxy("ALVideoDevice", IP, PORT)
# Use the bottom camera
camProxy.setParam(18, 1)

h, s, v, i = 2, 158, 144, 0	# hsv and its index
r, g, b, j = 55, 60, 144, 0	# rgb and its index
size = 0
counter = 0

def findBall():	
	# Get X and Y coordinates of the ball in the snapshot
	coords = getCoords()
	(x,y) = coords

	# Get the position of the bottomCamera and the head
	camBottom = motion.getPosition('CameraBottom', 2, True)
	head = motion.getAngles(["HeadPitch","HeadYaw"],True)
		
	# Check if the ball is found
	if(x != 0) and (y != 0):
		relcoords = calcPosition(coords, camBottom)
		(xPos, yPos, xAngle, yAngle) = relcoords
		snipe(head, xAngle, yAngle)
		snipe(head, xAngle, yAngle)
		
		# Commented code for showing the image
		# centeredim = getImageBGR()
		# cv.ShowImage("centered", centeredim) 
		# cv.WaitKey(0)
		# time.sleep(0.2)	

	else:
		relcoords = (0,0,0,0)
	
	return relcoords

def getCoords():
	posX, posY = 0, 0

	# Get a snapshot from the robot
	im = getImage()
	
	posArray = colourDetect(im)

	# Check whether the colourDetect has detected something
	if len(posArray) != 0:
		(posX, posY) = circleDetect(im, posArray)

	return (posX, posY)

def calcPosition(coord, cam):
    global size
    (width, height) = size

    # Coord with origin in the upperleft corner of the image
    (xCoord, yCoord) = coord

    # Change the origin to centre of the image
    xCoord = -xCoord + width/2.0
    yCoord = yCoord - height/2.0

    # Convert pixel coord to angle
    radiusPerPixel = 0.005061454830783556
    xAngle = xCoord * radiusPerPixel
    yAngle = yCoord * radiusPerPixel

    # The position (x, y, z) and angle (roll, pitch, yaw) of the camera
    (x,y,z, roll,pitch,yaw) = cam
    
    # Radius (in meters) of the ball in Webots
    # ballRadius = 0.0325
    
    # Radius (in meters) of the ball in real life  
    ballRadius = 0.065

    # Position of the ball where origin with position and rotation of camera
    xPos = (z-ballRadius) / tan(pitch + yAngle)
    yPos = tan(xAngle) * xPos

    # Position of the ball where origin with position of camera and rotation of body 
    xPos = cos(yaw)*xPos + -sin(yaw)*yPos
    yPos = sin(yaw)*xPos +  cos(yaw)*yPos

    # Position of the ball where origin with position and rotation of body
    xPos += x
    yPos += y

    return (xPos, yPos, xAngle, yAngle)

def getBallCircle(storage, output, posArray):
    global counter
    
    bestX, bestY, bestDistance, bestRadius = 0, 0, 1000, 0

    # X and Y output of the ColourDetection
    posColourX, posColourY = posArray[0]

    circles = np.asarray(storage)
    for circle in circles:
        Radius, x, y = int(circle[0][2]), int(circle[0][0]), int(circle[0][1])
        distance = fabs(posColourX - x) + fabs(posColourY - y)

        # Check if the radius is between the minimum and maximum value (in pixels) of the ball
        if (Radius >= 2 and Radius <= 24):
        	#cv.Circle(output, (x, y), 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
        	#cv.Circle(output, (x, y), Radius, cv.CV_RGB(255, 0, 0), 3, 8, 0)
	        
	        # We need the circle with the minimal distance to the output of the colourDetection
	        if distance < bestDistance:
	            bestX = x
	            bestY = y
	            bestDistance = distance
	            bestRadius = Radius
    
    # Calculate the distance between the point found in CircleDetection and the one from ColourDetection 
    absDistance = sqrt(pow(fabs(bestX - posColourX), 2) + pow(fabs(bestY - posColourY), 2))
    #print posColourX, posColourY, bestX, bestY, bestRadius, absDistance

    # Check if absDistance is smaller than the ball with a margin of 20%
    if absDistance  < (bestRadius * 1.2 ):         	
    	# CODE FOR SHOWING THE IMAGE WITH THE FOUND CIRCLE
    	# cv.Circle(output, (bestX, bestY), 1, cv.CV_RGB(0, 255, 0), -1, 8, 0)
    	# cv.Circle(output, (bestX, bestY), bestRadius, cv.CV_RGB(0, 0, 255), 3, 8, 0)
    	# cv.ShowImage("Circles", output) 
    	# cv.WaitKey(0)
    	return (bestX, bestY)
    else:
    	return (0, 0)  

def circleDetect(im, posArray):
	(width, height) = cv.GetSize(im)
	storage = cv.CreateMat(width, 1, cv.CV_32FC3)
	thresholded = cv.CreateImage(cv.GetSize(im),8,1)
	
	# Convert the image to grayscale
	cv.CvtColor(im, thresholded, cv.CV_BGR2GRAY)
	
	# Use Canny Edge Detection for detecting edges so that the Hough Circles will work better
	cv.Canny(thresholded, thresholded, 50, 100, 3)

	# Smooth to reduce noise a bit more
	cv.Smooth(thresholded, thresholded, cv.CV_BLUR, 3, 3)

	# Use HoughCircles to detect all the circles in the image
	cv.HoughCircles(thresholded, storage, cv.CV_HOUGH_GRADIENT, 2, thresholded.width/4, 10, 10, 0, 18)
	
	# Check if one of the circles is the ball
	(x, y) = getBallCircle(storage, im, posArray)

	return (x, y)

def colourDetect(im):
	global counter
	(width, height) = cv.GetSize(im)
	posx = 0
	posy = 0
	test = cv.CreateImage(cv.GetSize(im), 8, 3)
	imdraw = cv.CreateImage(cv.GetSize(im), 8, 3)
	
	# Filter the image
	thresh_img = filterImage(im)

	# Smooth the image and than erode the image for reducing noise	
	cv.Smooth(thresh_img, thresh_img, cv.CV_BLUR, 9, 9)
	cv.Erode(thresh_img, thresh_img, None, 1)

	thresholds = []
	# Check the whitest pixel and see if it's above the threshold
	threshold = checkThreshold(thresh_img)
	thresholds.append(threshold)

	# CODE FOR LOOPING THROUG THE CONTOURS (ONLY HAVE TO BE USED WHEN THERE ARE MUTIPLE ORANGE OBJECTS)
	# while threshold != (0,0):
	# 	contour = getContour(thresh_img, threshold)
	# 	if contour:
	# 		cv.DrawContours(thresh_img, contour, cv.ScalarAll(0), cv.ScalarAll(0), 0, cv.CV_FILLED)
	# 		#cv.ShowImage("output", thresh_img)
	# 		#cv.WaitKey(0)
	# 	else:
	# 		return thresholds
	# 	thresholds.append(threshold)
	# 	threshold = checkThreshold(thresh_img)
	# 	print threshold

	return thresholds

def getThresholdedImg(im):
	imghsv = cv.CreateImage(cv.GetSize(im),8,3)

	# Convert the image to HSV
	cv.CvtColor(im,imghsv,cv.CV_BGR2HSV)
	
	imgthreshold = cv.CreateImage(cv.GetSize(im),8,1)
	
	# Get all the pixels that are in the blue range
	cv.InRangeS(imghsv,cv.Scalar(110,100,100),cv.Scalar(120,180,180),imgthreshold)
	
	return imgthreshold

def getContour(thresh_img, maxLoc):
	(width, height) = cv.GetSize(thresh_img)
	storage = cv.CreateMemStorage(0)
	contours = cv.FindContours(thresh_img, storage, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE, (0,0))
	#contours, counter = cv2.findContours(thresh_img, storage, int(cv.CV_RETR_EXTERNAL), int(cv.CV_CHAIN_APPROX_SIMPLE),(0,0))
	testImage = cv.CreateMat(width, height, cv.CV_8UC3)

	if(maxLoc != (0,0)):
		(maxX, maxY) = maxLoc
		counter = 0
		while contours:
			if(cv.ContourArea(contours) > 25):
				#print counter
				counter += 1
				imContours = cv.CreateImage(cv.GetSize(thresh_img),8,3)
				for contour in list(contours):
					(x, y) = contour
					#print contour
				cv.DrawContours(imContours, contours, cv.ScalarAll(255), cv.ScalarAll(255), 0, cv.CV_FILLED)
				color = cv.Get2D(imContours, maxY, maxX)
				print color
				if color != (0, 0, 0, 0):
					#cv.ShowImage("ColourDetect", imContours) 
					#cv.WaitKey(0)
					return contours
			contours = contours.h_next()
			#print contours

def checkThreshold(thresh_img):
	# Get the whitest pixel of the image
	minMaxLoc = cv.MinMaxLoc(thresh_img)
	(minVal, maxVal, minLoc, maxLoc) = minMaxLoc
	
	# See if it's below the threshold
	if maxVal/256.0 < 0.2:
		# No ball is found
		return (0,0)
	# Ball could be found
	else:
		# cv.ShowImage("ColourDetect", thresh_img) 
		# cv.WaitKey(0)
		# Return the position of the found pixel 
		return maxLoc

def filterImage(im):
    # Size of the images
    (width, height) = size
    
    hsvFrame = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
    filter = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
    filter2 = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
    
    hsvMin1 = cv.Scalar(0,  90,  130, 0)
    hsvMax1 = cv.Scalar(12, 256, 256, 0)
    
    hsvMin2 = cv.Scalar(170,  90,  130, 0)
    hsvMax2 = cv.Scalar(200, 256, 256, 0)

    # Color detection using HSV
    cv.CvtColor(im, hsvFrame, cv.CV_BGR2HSV)
    cv.InRangeS(hsvFrame, hsvMin1, hsvMax1, filter)
    cv.InRangeS(hsvFrame, hsvMin2, hsvMax2, filter2)
    cv.Or(filter, filter2, filter)
    return filter

def getImage():
	global size
	
	videoClient = camProxy.subscribeCamera("python_client", 1, 0, 11, 30)
  # Get a camera image.
  # image[6] contains the image data passed as an array of ASCII chars.
	naoImage = camProxy.getImageRemote(videoClient)
  # Time the image transfer.
	camProxy.unsubscribe(videoClient)
  # Now we work with the image returned and save it as a PNG  using ImageDraw
  # package.

  # Get the image size and pixel array.
	ImageWidth = naoImage[0]
	ImageHeight = naoImage[1]
	array = naoImage[6]
	size= (ImageWidth,ImageHeight)
  # Create a PIL Image from our pixel array.
	img = Image.fromstring("RGB", (ImageWidth, ImageHeight), 	array)

	cv_im=cv.CreateImageHeader(img.size,cv.IPL_DEPTH_8U,3)
	cv.SetData(cv_im,img.tostring(),img.size[0]*3)
	cv.CvtColor(cv_im,cv_im,cv.CV_RGB2BGR)
	#img.save("camImage.png", "PNG")
	#cv_im = cv.LoadImage("camImage.png", 3)
	#img.show()
	#cv.ShowImage("Geconverteerd",cv_im)
	return cv_im

def snipe(head, xAngle, yAngle):
	[HeadPitch, HeadYaw] = head
	yAngle += HeadPitch
	xAngle += HeadYaw
	motion.setAngles(['HeadPitch', 'HeadYaw'], [yAngle, xAngle], 0.9)
	time.sleep(0.5)
	print 'sniped'

def findGoal():
	global posx, posy
	i = 0
	Pixel = []
	Detect = []
	GoalDetect = (0, 0)
	Found = False
	while Found == False:
	  	im = getImage()
		cv.Flip(im,im,1)				# Horizontal flipping for synchronization, comment it to see difference.
		imdraw = cv.CreateImage(cv.GetSize(im),8,3)	# We make all drawings on imdraw.
		thresh_img = getThresholdedImg(im)	
		cv.ShowImage("test", thresh_img)	# We get coordinates from thresh_img
		cv.WaitKey(33)
		cv.Erode(thresh_img, thresh_img,None,1)		# Eroding removes small noises
		(leftmost,rightmost,topmost,bottommost) = getpositions(thresh_img)
		#print ( getpositions(thresh_img))
		if (leftmost-rightmost != 0) or (topmost-bottommost != 0):
			lastx = posx
			lasty = posy
			posx = cv.Round((rightmost + leftmost) / 2)
			posy = cv.Round((bottommost + topmost) / 2)
		GoalDetect = (posx, posy)
		print cv.CountNonZero(thresh_img)
		if GoalDetect == 0,0):
			MoveToGoal() 
		else:
			pixelValue = cv.CountNonZero(thresh_img)
			Pixel.append(pixelValue)
			i += 1
			print "not null"
			return
			if i == 10:
				avg = sum(Pixel)/len(Pixel)
				del Pixel[:]
				print "average"
				print avg
				i = 0
				if avg > 5:
					Found = True
					print 'Found Goal'
		if cv.WaitKey(33) == 1048603:			# exit if Esc key is pressed
			break

    # get robot position before move

def MoveToGoal():
    #while( coordinates are in middle of screen ):
   motion.walkTo( 0,-0.09,0 )
   motion.walkTo( 0,0,0.415 )


'''

PARAMETERS OF THE SUBSCRIBECAMERA
-----------------------------------------------------------------------------------

method: camProxy.subscribeCamera("python_client", camera, resolution, colorSpace, 5)

camera
0 				TopCamera
1               BottomCamera

resolution      width, height
0               160, 120
1               320, 240
2               640, 480

colorSpace      type
0               kYuv
9               kYUV422
10              kYUV
11              kRGB
12              kHSY
13              kBGR

space           type
0               SPACE_TORSO
1               SPACE_WORLD
2               SPACE_NAO


CALCULATION OF RADIANS PER PIXEL
-----------------------------------------------------------------------------------

Height of image is 120
angle of image in height is 34.80 degrees
34.80 degrees = 0.6073745796940266 radians
radians per pixel = 0.6073745796940266 / 120 = 0.005061454830783556 

'''