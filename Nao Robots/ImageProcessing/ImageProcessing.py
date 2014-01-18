import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import ColorSysCustom as csc
from cv2 import cv

ONE_OVER_255 = 1.0 / 255.0
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLACK = (0, 0, 0)

# TODO: remove unused imports

# DENNIS OPT: save function pointers to functions which are often used inside loops
CAST_DOUBLE = np.double
RGB_TO_HUE = csc.rgb_to_hue

class ImageProcessing():
    
    def __init__(self, imgString): 
        imgTemp = Image.open(imgString)
        self.height, self.width = imgTemp.size
        self.img = cv2.imread(imgString)
        self.maxSpacing = 10
        self.minYellow = 100
        self.goalpostSpacingSquared = 50*50
        self.LOWER_BOUND_GREEN = 0.0
        self.UPPER_BOUND_GREEN = 0.85
        self.LOWER_BOUND_YELLOW = 0.08333
        self.UPPER_BOUND_YELLOW = 0.25
               
                
    # width of image, height of image, image, fraction of the image to be randomly taken pixels from            
    def getAverageLightIntensity(self, width, height, img, fractionOfImage):   
        light_sum = 0;      # DENNIS: renamed sum to light_sum, just to be safe
        self.n = np.int(fractionOfImage*width*height)
            
        randomsX = np.random.uniform(0, np.int(width), size = self.n)
        randomsY = np.random.uniform(0, np.int(height), size = self.n)
        
        for i in xrange(0, self.n):   
            B, G, R = img[randomsX[i]][randomsY[i]]
                
            # fitting them for HSV transform
            # DENNIS OPT: on most processors, multiplication is much cheaper than division. So multiply by 1/255 instead of dividing by 255
            R = CAST_DOUBLE(R) * ONE_OVER_255
            G = CAST_DOUBLE(G) * ONE_OVER_255
            B = CAST_DOUBLE(B) * ONE_OVER_255
            
            light_sum  += ( (max(R, G, B) + min(R, G, B)) * 0.5 )     # DENNIS OPT: csc.rgb_to_luminance was such a short function that inlining is better
            # L = csc.rgb_to_luminance(R, G, B)
            # light_sum = light_sum + L
            
        self.Lic = (light_sum/self.n)
        
        
    def setThreshold(self, t):
        self.threshold = t
        self._255_MIN_THRESHOLD = 255 - self.threshold
        
    def getThreshold(self):
        return self.threshold
   
   
    def startLumi(self):    
        self.new_img = Image.new('RGB', (self.height, self.width), "black")     # TODO: I dont believe this self.new_img is used anywhere. safe to remove?
        #pixels = self.img.load()
        
        # DENNIS OPT: save fields of self which are used inside the inner loop (= very often) in local variables. 
        #             Python accesses these much quicker
        img = self.img
        height = self.height
        threshold = self.threshold
        _255_MIN_THRESHOLD = self._255_MIN_THRESHOLD
        Lic = self.Lic
        LOWER_BOUND_YELLOW = self.LOWER_BOUND_YELLOW
        UPPER_BOUND_YELLOW = self.UPPER_BOUND_YELLOW
        LOWER_BOUND_GREEN = self.LOWER_BOUND_GREEN
        UPPER_BOUND_GREEN = self.UPPER_BOUND_GREEN
        
        for x in xrange(0, self.width):
            for y in xrange(0, height):
                B, G, R = img[x][y]
               
                #Getting the Hue and Lum
                R = CAST_DOUBLE(R) * ONE_OVER_255     # DENNIS OPT: mult by 1/255 instead of dividing by 255
                G = CAST_DOUBLE(G) * ONE_OVER_255
                B = CAST_DOUBLE(B) * ONE_OVER_255
                H = RGB_TO_HUE(R, G, B)
                Y = ( (max(R, G, B) + min(R, G, B)) * 0.5 )     # DENNIS OPT: inlined csc.rgb_to_luminance
                
                '''
                TODO: Inside these loops, we're changing self.img forever to only consist of 4 possible colors
                (white, red, green and black)
                
                We should instead create an enumeration of only those 4 colors (4 properly named ints for example, instead of 3-tuples)
                That'll allow for MUCH faster comparison of colors (checking if a pixel has a certain color will be only a single
                comparison instead of 3 comparisons)
                '''
                
                #accepted white
                if((Y*255 > threshold + _255_MIN_THRESHOLD*Lic)):                  # DENNIS OPT: inlined acceptedLumi, precompute 255 - threshold
                    img[x, y] = COLOR_WHITE                                        # DENNIS OPT: predefine COLOR_WHITE instead of reconstructing it every iteration
                elif((H >= LOWER_BOUND_YELLOW and H <= UPPER_BOUND_YELLOW)):       # DENNIS OPT: inlined acceptedYellow
                    img[x, y] = COLOR_RED                                          # DENNIS OPT: predefine COLOR_RED instead of reconstructing it every iteration
                elif((H >= LOWER_BOUND_GREEN and H <= UPPER_BOUND_GREEN)):         # DENNIS OPT: inlined acceptedGreen
                    img[x, y] = COLOR_GREEN                                        # DENNIS OPT: predefine COLOR_GREEN instead of reconstructing it every iteration
                else:
                    img[x, y] = COLOR_BLACK                                        # DENNIS OPT: predefine COLOR_BLACK instead of reconstructing it every iteration
                    
        self.calculateGoalposts()
        self.removeBackGround()


    def calculateGoalposts(self):
        
        self.goalposts = []
        self.goalpostsTemp = []
        
        '''
        TODO: can probably massively improve this by:
        
            Making inner loop reverse automatically instead of making it go up first and every iteration compute reverse
            
            Maybe (???) cache results of [yy+1], [yy+2] and [yy+3] and shift those values and only compute a single value every iteration?
            This is complicated though and probably much less necessary if we've done the TODO above
        '''
        
        # DENNIS OPT: save fields of self which are used inside the inner loop (= very often) in local variables. 
        #             Python accesses these much quicker
        width = self.width
        img = self.img
        minYellow = self.minYellow
        append_goalpostsTemp = self.goalpostsTemp.append        # DENNIS OPT: I like function pointers
        
        for x in xrange(20, self.height-20):
            count = 0
            for y in xrange(0, width):
                #reverse y
                yy = width-y-1
                B, G, R = img[yy][x]
                #if goalpost pixel
                if(R == 0 and B == 255):
                    if (count == 0):
                        if (yy+3 < width):
                            B1, G1, R1 = img[yy+1][x]
                            B2, G2, R2 = img[yy+2][x]
                            B3, G3, R3 = img[yy+3][x]
                            #if either one of the previous ones are green
                            if((B1 == 0 and G1 == 255) and (B2 == 0 and G2 == 255) and (B3 == 0 and G3 == 255)):
                                count = count + 1
                    else:
                        count = count + 1
                        if(count > minYellow):
                            append_goalpostsTemp([x, yy+count])
                            break
                else:
                    count = 0
        
        #removing points close to each other
        
        if (len(self.goalpostsTemp) > 0):
            
            self.goalposts.append(self.goalpostsTemp[0])
            
            for i in xrange(1, len(self.goalpostsTemp)):
                xt, yt = self.goalpostsTemp[i]
                double = False
                for j in xrange(0, len(self.goalposts)):
                    x, y = self.goalposts[j]
                    dx = x-xt
                    dy = y-yt
                    if((dx*dx + dy*dy) < self.goalpostSpacingSquared):        # DENNIS OPT: compute dx and dy, 2 subtractions less each iteration
                        double = True
                        break
                if(not double):
                    self.goalposts.append(self.goalpostsTemp[i])
        
        
        if (len(self.goalposts) > 2):
            self.goalposts = []
            
        # clean goalpostsTemp from memory
        self.goalpostsTemp = None
    
                
    def getGoalposts(self):
        return self.goalposts

    def removeBackGround(self):
        #self.white_list = []
        
        # DENNIS OPT: save fields of self which are used inside the inner loop (= very often) in local variables. 
        #             Python accesses these much quicker
        w = self.getHeightImage()
        h = self.getWidthImage()
        img = self.img
        maxSpacing = self.maxSpacing
        for x in xrange(0, w):
            count = 0
            
            for y in xrange(0, h):
                B, G, R = img[y][x]
                if(B == 0 and G == 255):
                    count = count + 1
                else:
                    count = 0
                if(count > maxSpacing):
                    for r in xrange(0, y-count+1):
                        img[r, x] = COLOR_BLACK        # DENNIS OPT: use predefined COLOR_BLACK
                    break
            if(count <= maxSpacing):
                for y in xrange(0, h):
                    img[y, x] = COLOR_BLACK            # DENNIS OPT: use predefined COLOR_BLACK
                
        #self.clusterImage()
        self.onlyWhite()
        #self.abstractImage()
        
    '''
    def clusterImage(self):
        clusterSize = 1 #self.getHeightImage()/30
        self.clusterpoins = []
        h = self.getWidthImage()
        samples = h*2 #h*np.int(clusterSize/3)
        
        for x in xrange(0, self.getHeightImage()):
            
            tempPoints = []
            nrClusters = 0
            
            for i in xrange(0, np.int(samples)):
                
                rx = np.random.random()*clusterSize + x*clusterSize
                ry = np.random.random()*h
                
                #check if white
                B, G, R = self.img[ry][rx]
                if (B == 255 and G == 255 and R == 255):
                    
                    #if there are no points assigned yet:
                    if (len(tempPoints) is 0):
                        tempPoints.append([0, rx, ry])
                    #else go though the individual clusters and check where it belongs to, if it doesn't belong to any, make a new cluster
                    else:
                        close = False
                        for c in xrange(0, len(tempPoints)):
                            cn, cx, cy = tempPoints[c]
                            if(np.abs(ry - cy) <= self.maxSpacing):
                                close = True
                                tempPoints.append([cn, rx, ry])
                                break
                        if(close is False):
                            nrClusters = nrClusters + 1
                            tempPoints.append([nrClusters, rx, ry])
            
            #averaging the clusterpoints and add to clusterlist
            if (len(tempPoints) is not 0):
                for i in xrange(0, nrClusters + 1):
                    xsum = 0
                    ysum = 0
                    n = 0
                    for j in xrange(0, len(tempPoints)):
                        cn, cx, cy = tempPoints[j]
                        if(cn is i):
                            n = n + 1
                            xsum = xsum + cx
                            ysum = ysum + cy
                    self.clusterpoins.append([xsum/n, ysum/n])
        self.finalizeImage()
    '''   
       
    '''    
    def abstractImage(self):
        
        self.clusterpoins = []
        w = self.getHeightImage()
        h = self.getWidthImage()
        
        for x in xrange(0, np.int(w)):
            whitesV = []
            whitesH = []
            self.y = 0
            
            while self.y < np.int(h):
                #check if white
                B, G, R = self.img[self.y][x]
                if (B == 255):
                    whitesV.append([x, self.y])
                    whitesH.append([x, self.y])
                    #if white, check next ones until there are no more whites and average the point
                    
                    #horizontal (x)
                    for x2 in xrange(1, x-1):
                        B, G, R = self.img[self.y][x-x2]
                        if (B == 255):
                            whitesH.append([x-x2, self.y])
                        else:
                            break
                    for x3 in xrange(1, np.int(h)-x-1):
                        B, G, R = self.img[self.y][x+x3]
                        if (B == 255):
                            whitesH.append([x+x3, self.y])
                        else:
                            break
                    
                    #vertical (y)
                    self.yy = np.int(h)-1   
                    for y2 in xrange(self.y+1, np.int(h)):
                        B, G, R = self.img[y2][x]
                        if (B == 255):
                            whitesV.append([x, y2])
                        else:
                            self.yy = y2
                            break
                        
                    #checking for shortest length:
                    #print(len(whitesV), len(whitesH), x, self.y)
                    if (len(whitesV) < len(whitesH)):
                        self.y = self.yy
                        sumX = 0
                        sumY = 0
                        for i in xrange(0, len(whitesV)):
                            sumX = sumX + whitesV[i][1]
                            sumY = sumY + whitesV[i][0]
                        self.clusterpoins.append([sumX/len(whitesV), sumY/len(whitesV)])
                        
                    else:
                        sumX = 0
                        sumY = 0
                        for j in xrange(0, len(whitesH)):
                            sumX = sumX + whitesH[j][1]
                            sumY = sumY + whitesH[j][0]
                        self.clusterpoins.append([sumX/len(whitesH), sumY/len(whitesH)])
                        
                    #cleaning up the mess this made:
                     
                     
                    whitesH = []
                    whitesV = []
                    
                self.y = self.y + 1
                
        self.finalizeImage()
    '''
        
    '''    
    def finalizeImage(self):
        for x in xrange(0, self.getWidthImage()):
            for y in xrange(0, self.getHeightImage()):
                self.img[x, y] = (0, 0, 0)
        for c in xrange(0, len(self.clusterpoins)):
            self.img[self.clusterpoins[c][1], self.clusterpoins[c][0]] = (255, 255, 255)
    '''    
        
    def onlyWhite(self):
        # DENNIS OPT: save fields of self which are used inside the inner loop (= very often) in local variables. 
        #             Python accesses these much quicker
        height = self.getHeightImage()
        img = self.img
        for x in xrange(0, self.getWidthImage()):
            for y in xrange(0, height):
                B, G, R = img[x][y]
                if not(B == 255 and G == 255):
                    img[x, y] = COLOR_BLACK                # DENNIS OPT: use predefined COLOR_BLACK
    
    # DENNIS OPT: commented the 3 accepted_ methods, since they're simple enough to manually inline
    '''
    def acceptedLumi(self, Y):
        #Y in [0, 255]
        if (Y > self.threshold + (255-self.threshold)*self.Lic):
            return True
        return False
    
    
    def acceptedGreen(self, H):
        #H in [0, 255]
        #if (H >= 0.222222 and H <= 0.466667):
        if (H >= self.LOWER_BOUND_GREEN and H <= self.UPPER_BOUND_GREEN):
            return True
        return False
    
    def acceptedYellow(self, H):
        #H in [0, 255]
        #if (H >= 0.222222 and H <= 0.466667):
        if (H >= self.LOWER_BOUND_YELLOW and H <= self.UPPER_BOUND_YELLOW):
            return True
        return False
    '''
    
    def getClusterPoints(self):
        return self.clusterpoints
   
   
    def getImage(self):
        return self.img
    
    
    def getWidthImage(self):
        return self.width  
    
    
    def getHeightImage(self):
        return self.height
        
        
    def getLightIntensityScalar(self):
        return self.Lis
    
    
    def getSortedWhites(self):
        return self.white_list
  