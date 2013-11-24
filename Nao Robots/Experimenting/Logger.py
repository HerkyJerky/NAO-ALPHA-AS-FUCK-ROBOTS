__author__ = 'redsphinx'

# format saved data:
# timestamp_action_parameter1_parameter2_..._parameterN
# each on a new line

# actions: 1 stand(), 2 sit(), 3 move(x,y,theta,speed), 4 stop(), 5 takePic(name), 6 slam(), 7 analyze(), 8 talk(word)

import time

path = "log.txt"

class Logger:
    def __init__(self):

        pass

    def logWrite(self, content):
        log = open(path, "r")
        prevCont = log.read()
        log.close()
        log = open(path, "w")
        log.write(prevCont + "\n" + content)
        log.close()
        log = open(path, "r")
        prevCont = log.read()
        print(prevCont)
        log.close()
        pass

    def logDelAll(self):
        open(path, 'w').close()
        pass

    def getData(self):
        log = open(path, "r")
        prevCont = log.read()
        log.close()
        return prevCont
        pass

    def getLastEntry(self):
        log = open(path, "r")
        lines = log.readlines()
        lastEntry = lines[-1]
        return lastEntry
        pass

logger = Logger()
logger.logDelAll()
#logger.logWrite(time.time().__str__() + "_3_{0}_{1}_{2}_{3}".format("je mma","whoho","yay","bro"))
