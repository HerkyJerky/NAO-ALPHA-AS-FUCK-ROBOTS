__author__ = 'redsphinx'
'''
make panel with live map and where the robot thinks it is


'''


from Tkinter import *
import numpy as np
import math

#controller = MapControl()
FIELDX = 400  # measured in cm
FIELDY = 300+150  # measured in cm (plus other half of field)
OFFSET = 25 # don't think i'll use it
alpha = 5  # thickness of lines
beta = 2  # ?
# all actual coordinates of the cornerpoints on the field
A = [0, 0]
B = [90, 0]
C = [90, 60]
D = [310, 60]
E = [310, 0]
F = [400, 0]
G = [400, 300]
H = [0, 300]
I = [200, 300]
J = [200, 180]
K = [130, 0]
L = [270, 0]
ACT_LNDMRKS = [A, B, C, D, E, F, G, H, J, K, L]

# acceptable region. the minimal distance between two cornerpoints [LE for example] is 40 cm. so radius is then 20 cm
# the detected landmark must be within this region to be accepted as a well observed landmark
OKRADIUS = 20 # in cm
DEG2RAD = math.pi/180.0 # Convert Deg to Rad
'''

*** = OFFSET
        ....................................
        .                             *    .
        .           fieldx        *    .
        .     ------o--------o------- * * *.
        .  f |                       |     .
        .  i |                       |     .
        .  e |                       |     .
        .  l |                       |     .
        .  d |                       |     .
        .  y |_______________________|     .
        .    |                       |     .
'''

root = Tk()
#root.wm_title("[ALPHA] - Simultaneous Localization And Mapping")
#root.configure(bg='black')
#frame = Frame(root, bg='black', width=600, height=400)

'''
output is [output[0],output[1]]
output[0] are poses and they are of this format : [x,y,theta]
output[1] are landmark positions of this format : [x,y]                                                                                                                                                                                                                                                                                                                                                                                                  `    `
'''

class MapViewer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("[ALPHA] - SLAM")
        self.pack(fill=BOTH, expand=1)
        self.makeLinesOnField()
        theta = float(45*DEG2RAD)
        output = [[[200, 100, theta]], [[80, 50, False], [320, 70, False], [140, 10, True], [320, 15, False]]]
        self.boolTest(0)
        self.updateMapNew(output)
        #print output
        #self.updateMapNew(output)
        #print self.normalizeOutputSLAM(output)
        root.geometry("400x450")
        root.mainloop()
        pass




    # old method for updating the map
    def updateMap(self, output):
        # create a pixel representing the robot
        self.drawAt(output[0], output[1], 'blue')
        #self.canvas.create_rectangle(output[0], output[1], output[0]+2, output[1]+2, fill='black')
        # create all the landmarks pixels
        for i in xrange(3, len(output), 2):
            self.drawAt(output[i], output[i+1], 'white')
            #self.canvas.create_rectangle(output[i], output[i + 1], output[i]+2, output[i + 1]+2, fill='red')

        #self.canvas.pack(fill="both", expand=1)
        pass
    
    '''
    output is [output[0],output[1]]
    output[0] are poses and they are of this format : [x,y,theta]
    output[1] are landmark positions of this format : [x,y]                                                                                                                                                                                                                                                                                                                                                                                                  `    `
    '''

    def updateMapNew(self, output):
        poses = output[0]
        landmarks = output[1]
        # draw robot
        for i in range(len(poses)):
            self.drawAt(poses[i][0], poses[i][1], poses[i][2], 'blue', 'robot')

        # draw landmarks
        for k in range(len(landmarks)):
            if (landmarks[k][2] is True):
                self.drawAt(landmarks[k][0], landmarks[k][1], 0, '#ffa200', 'landmark')
            if (landmarks[k][2] is False):
                self.drawAt(landmarks[k][0], landmarks[k][1], 0, '#ff00ae', 'landmark')
        pass

    '''
    output is [output[0], output[1]]
    output[0] are poses and they are of this format : [x, y, theta]
    output[1] are landmark positions of this format : [x, y, bool]                                                                                                                                                                                                                                                                                                                                                                                                  `    `
    '''
    # normalize the output of SLAM
    def normalizeOutputSLAM(self, output): # TODO 0 1 are false true, so check for this instead of checking for booleans
        minX = float('inf')
        minY = float('inf')
        poses = output[0]
        landmarks = output[1]
        # check for the minX and minY
        for i in xrange(0, len(poses)):
            if poses[i][0] < minX:
                minX = poses[i][0]
            elif poses[i][1] < minY:
                minY = poses[i][1]
            else:
                print 'something wrong with getting poses coordinates'

        for i in xrange(0, len(landmarks)):
            if landmarks[i][0] < minX:
                minX = landmarks[i][0]
            elif landmarks[i][1] < minY:
                minY = landmarks[i][1]
            else:
                print 'something wrong with getting landmarks coordinates'

        # how much we have to move each
        moveX = 0 - minX
        moveY = 0 - minY

        # move them
        for i in xrange(0, len(poses)):
            poses[i][0] += moveX
            poses[i][1] += moveY

        for i in xrange(0, len(landmarks)):
            landmarks[i][0] += moveX
            landmarks[i][1] += moveY

        normalizedOutput = [poses, landmarks]
        return normalizedOutput


    def drawAt(self, x, y, theta, color, mode):
        if mode == 'robot':
            alp1 = [x-7, y-14]
            bet1 = [x-7, y+14]
            gam1 = [x+7, y]
            center = [x, y]
            alp = self.rotate(alp1, center, theta)
            bet = self.rotate(bet1, center, theta)
            gam = self.rotate(gam1, center, theta)
            self.canvas.create_polygon(alp[0], alp[1], bet[0], bet[1], gam[0], gam[1], fill=color, outline='black', width=1)
            self.canvas.pack(fill="both", expand=1)
            pass
        else:
            if (x - alpha > 0) and (x + alpha < FIELDX):
                if (y - alpha > 0) and (y + alpha < FIELDY):
                    self.canvas.create_oval(x-2, y-2, x+4, y+4, fill=color, outline='black', width=1)
                    self.canvas.pack(fill="both", expand=1)
                else:
                    print("please enter {0} > y > {1}".format(FIELDY-2, 2))
            else:
                print("please enter {0} > x > {1}".format(FIELDX-2, 2))

    def rotate(self, coor, center, theta):
        theta = -theta
        newX = center[0] + ((coor[0]-center[0])*math.cos(theta) - (coor[1]-center[1])*math.sin(theta))
        newY = center[1] + ((coor[0]-center[0])*math.sin(theta) + (coor[1]-center[1])*math.cos(theta))
        return [int(newX), int(newY)]

    def makeLinesOnField(self):
        self.canvas = Canvas(self)
        self.canvas.create_rectangle(0, 0, FIELDX, FIELDY, fill='#006400')
        self.drawOKRADIUS([A, B, C, D, E, F, G, H, J], '#00a300')
        self.canvas.pack(fill="both", expand=1)
        self.drawOKRADIUS([K, L], '#c9c902')
        self.canvas.pack(fill="both", expand=1)
        self.canvas.create_rectangle(A[0], A[1], G[0], G[1], fill=None, width=5, outline='white')
        self.canvas.pack(fill="both", expand=1)
        self.canvas.create_rectangle(B[0], B[1], D[0], D[1], fill=None, width=5, outline='white')
        self.canvas.pack(fill="both", expand=1)
        self.canvas.create_rectangle(J[0]-2, J[1]-2, J[0]+2, J[1]+2, fill='white', outline='white')
        self.canvas.pack(fill="both", expand=1)
        self.canvas.create_oval(140, 240, 260, 360, fill=None, width=5, outline='white')
        self.canvas.pack(fill="both", expand=1)

    def drawOKRADIUS(self, lndmrk, color):
        for i in xrange(len(lndmrk)):
            x = lndmrk[i][0]
            y = lndmrk[i][1]
            print x, y
            self.canvas.create_oval(x-OKRADIUS, y-OKRADIUS, x+OKRADIUS, y+OKRADIUS, fill=color, width='0')
            self.canvas.pack(fill="both", expand=1)

    def boolTest(self, answer):
        if answer is False:
            print 'answer is true'
        else:
            print 'answer is not valid'

    # approximate where the robot thinks it is on the field by finding a pattern that could match the actual landmarks
    def findPattern(self, normalizedOutput):

        pass

mappie = MapViewer(root)

