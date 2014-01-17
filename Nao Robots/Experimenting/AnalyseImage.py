import Distance as distance


class AnalyseImage:
    
    #insert angle in degrees
    def __init__(self):
        self.data = []
        #self.angle = a
    
    def analyse(self, imageName, a):
        self.d = distance.Distance(imageName, a)
        return self.d.getData()

#an = AnalyseImage()
##dat = [(double distance (in meter), double theta (in rad)), boolean goalpost......]
#dat = an.analyse('analyzeThis.png')
#print(dat)