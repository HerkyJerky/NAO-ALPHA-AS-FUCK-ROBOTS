from naoqi import ALProxy


IP = "192.168.200.17"
PORT = 9559


class MoveShit:
    def __init__(self):
        self.proxy = ALProxy("ALMotion", IP, PORT)
        self.proxy.setStiffnesses("Body", 1.0)
        self.proxy.walkInit()

    def setStep(self, lName, X, Y, Theta):
        legName  = [lName]
        footSteps = [[X, Y, Theta]]
        timeList = [1]
        clearExisting = False
        self.proxy.setFootSteps(legName, footSteps, timeList, clearExisting)

    def walkAlot(self, steps):
        for i in xrange(0, steps):
            if (i % 2 == 0):
                self.setStep("RLeg", 0, 5, 0)
            else:
                self.setStep("LLeg", 0, 5, 0)

moveShit = MoveShit()
moveShit.walkAlot(10)



## A small step forwards and anti-clockwise with the left foot
#legName = ["LLeg", "RLeg"]
#X       = 10
#Y       = 20
#Theta   = 0
#footSteps = [[X, Y, Theta], [X, -Y, Theta]]
#timeList = [1, 2]
#clearExisting = False
#proxy.setFootSteps(legName, footSteps, timeList, clearExisting)

