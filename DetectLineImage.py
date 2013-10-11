import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import math

class DetectLineImage():
    
    def __init__(self, imgString, threshold): 
        imgTemp = Image.open(imgString)
        height, width = imgTemp.size
        img = cv2.imread(imgString)
        self.threshold = threshold
        self.start(width, height, img)
        
    def start(self, width, height, img):    
        white_array = []
        for x in xrange(0, width):
            for y in xrange(0, height):
                pixel = img[x][y]
                if(self.accepted(pixel[0], pixel[1], pixel[2])):
                    white_pixel = [x, y]
                    white_array.append(white_pixel)
        self.newImg = self.createImage(width, height, white_array)
    
    #Eucledian distance of white and pixel we're reading
    def accepted(self, X, Y, Z):
    #white = [255, 255, 255]
        D = math.sqrt((255-X)*(255-X) + (255-Y)*(255-Y) + (255-Z)*(255-Z))
        if D <= self.threshold:
            return True
        return False

    def createImage(self, width, height, white_array):
        new_image = Image.new('RGB', (height, width), "black")
        pixels = new_image.load()
        for i in xrange(0, len(white_array)):
            coordinate = white_array[i]
            pixels[coordinate[1], coordinate[0]] = (255,255,255)
        return new_image
        
    def getNewImage(self):
        return self.newImg 
    
    def getThreshold(self):
        return self.threshold

#End of class

#Example code to illustrate this class' use
dli = DetectLineImage('Nao_Image.png', 250)
img = dli.getNewImage()
threshold = dli.getThreshold()
plt.title("Threshold = " + str(threshold))
plt.imshow(img)
plt.show()    
