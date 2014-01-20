__author__ = 'redsphinx'


# format saved data:
# timestamp_action_parameter1_parameter2_..._parameterN
# each on a new line

# actions: 1 stand(), 2 sit(), 3 move(x,y,theta,speed), 4 stop(), 5 takePic(name), 6 slam(), 7 analyze(),
# 8 talk(word), 9 moveHeadPitch(theta, speed), 10 lieDownRelax()


path = "log.txt"

class Logger:
    def __init__(self):

        pass

    def logWrite(self, content):
        log = open(path, "r")
        prevCont = log.read()
        log.close()
        log = open(path, "w")
        log.write(prevCont + content + "\n")
        log.close()
        log = open(path, "r")
        prevCont = log.read()
        #print(prevCont)
        log.close()

    def logDelAll(self):
        open(path, 'w').close()

    def getData(self):
        log = open(path, "r")
        prevCont = log.read()
        log.close()
        return prevCont

    def getLastEntry(self):
        log = open(path, "r")
        lines = log.readlines()
        lastEntry = lines[-1]
        return lastEntry

#logger = Logger()
#logger.logDelAll()
