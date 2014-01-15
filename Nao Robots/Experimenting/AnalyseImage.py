import Distance as distance


class AnalyseImage:
    
    #insert angle in degrees
    def __init__(self, a):
        self.data = []
        self.angle = a
    
    def analyse(self, imageName):
        self.d = distance.Distance(imageName, self.angle)
        return self.d.getData()
    
    
    
an = AnalyseImage()
#dat = [(boolean goalpost, double distance (in meter), double theta (in rad)), ......]
dat = an.analyse('analyzeThis.png')
print(dat)