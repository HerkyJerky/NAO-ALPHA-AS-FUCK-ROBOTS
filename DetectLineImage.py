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
        self.new_img = Image.new('RGB', (height, width), "black")
        pixels = self.new_img.load()
        for x in xrange(0, width):
            for y in xrange(0, height):
                pixel = img[x][y]
                if(self.accepted(pixel[0], pixel[1], pixel[2])):
                    pixels[y, x] = (255,255,255)
    
    #Eucledian distance of white and pixel we're reading
    def accepted(self, X, Y, Z):
    #white = [255, 255, 255]
        D = math.sqrt((255-X)*(255-X) + (255-Y)*(255-Y) + (255-Z)*(255-Z))
        if D <= self.threshold:
            return True
        return False
     
    def getNewImage(self):
        return self.new_img 
    
    def getThreshold(self):
        return self.threshold

#End of class

#Example code to illustrate this class' use
dli = DetectLineImage('Nao_Image2.png', 200)
img = dli.getNewImage()
threshold = dli.getThreshold()
plt.title("Threshold = " + str(threshold))
plt.imshow(img)
plt.show()    
