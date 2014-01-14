import Distance as distance


class AnalyseImage:
    
    
    def __init__(self):
        self.data = []
    
    def analyse(self, imageName):
        self.d = distance.Distance(imageName)
        return self.d.getData()
    
    
    
an = AnalyseImage()
dat = an.analyse('9jan03-7.png')
#print(dat)