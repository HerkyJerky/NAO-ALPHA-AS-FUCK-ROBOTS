__author__ = 'redsphinx'
'''
make panel with live map and where the robot thinks it is


'''


from Tkinter import *
import numpy as np
from MapControl import MapControl

#controller = MapControl()
FIELDWIDTH = 600  # measured in cm
FIELDHEIGHT = 400  # measured in cm
OFFSET = 25

'''

*** = OFFSET
        ....................................
        .                             *    .
        .           fieldWidth        *    .
        .     ------o--------o------- * * *.
        .  h |                       |     .
        .  e |                       |     .
        .  i |                       |     .
        .  g |                       |     .
        .  h |                       |     .
        .  t |_______________________|     .
        .    |                       |     .
'''

root = Tk()
#root.wm_title("[ALPHA] - Simultaneous Localization And Mapping")
#root.configure(bg='black')
#frame = Frame(root, bg='black', width=600, height=400)

class MapViewer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("[ALPHA] - Simultaneous Localization And Mapping")
        self.pack(fill=BOTH, expand=1)
        self.updateMap([50, 50, 5, 100, 101, 100, 105, 100, 109, 100, 113])
        root.geometry("600x400")
        self.parent.configure(bg='#006400')
        root.mainloop()
        pass


    # get output from SLAM about what cells to update
    # [x_robot, y_robot, theta_robot, x_landmark_1, y_landmark_1, x_landmark_2, ..., x_landmark_n, y_landmark_n]
    # TODO what is the unit of the coordinates? In cm
    def updateMap(self, output):  # TODO get actual output
        print output
        self.canvas = Canvas(self)
        # create a pixel representing the robot
        self.canvas.create_rectangle(output[0], output[1], output[0]+2, output[1]+2, fill='black')

        # TODO robot theta

        # create all the landmarks pixels
        for i in xrange(3, len(output), 2):
            self.canvas.create_rectangle(output[i], output[i + 1], output[i]+2, output[i + 1]+2, fill='red')

        self.canvas.pack(fill="both", expand=1)
        pass

        #test
mappie = MapViewer(root)


