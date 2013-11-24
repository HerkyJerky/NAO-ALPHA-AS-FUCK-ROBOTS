__author__ = 'redsphinx'

from Tkinter import *
from Motion import Motion
from Vision import Vision
from SlamStuff import SlamStuff
from Logger import Logger

root = Tk()
root.wm_title("Alpha as FUCK!")
root.configure(background='black')
frame = Frame(root, width=700, height=500)
motionObj = Motion()
visionObj = Vision()
slamObj = SlamStuff()
logObj = Logger()

class GUI:
    def __init__(self):
        frame.pack_propagate(0)
        self.createbuttons()
        frame.pack()
        root.mainloop()
        pass

    def meth(self, word):
        print word
        pass

    def createbuttons(self):
        standButton = Button(frame, text="stand up", background="orange", foreground="black", command= lambda : self.wrapper(motionObj.stand()))#lambda: motionObj.stand())
        standButton.pack()
        sitButton = Button(frame, text="sit down", background="orange", foreground="black", command=lambda: self.wrapper(motionObj.sit()))#motionObj.sit())
        sitButton.pack()
        moveButton = Button(frame, text="move", background="orange", foreground="black",
                            command=lambda:  self.wrapper(motionObj.move(self.moveX.get(), self.moveY.get(), self.moveTh.get(), self.moveFr.get())))
        moveButton.pack()
        self.makeXEntry()
        self.makeYEntry()
        self.makeThEntry()
        self.makeFrEntry()
        stopButton = Button(frame, text="STOP!", background="red", foreground="black", command=lambda : self.wrapper(motionObj.stop()))
        stopButton.pack()
        picButton = Button(frame, text="take picture", background="orange", foreground="black",
                           command=lambda: self.wrapper(visionObj.takePic(self.name.get())))
        picButton.pack()
        self.makeNameEntry()
        slamButton = Button(frame, text="SLAM", background="orange", foreground="black", command=lambda: self.meth("slam"))
        slamButton.pack()
        # yze
        analButton = Button(frame, text="analyze", background="orange", foreground="black", command=lambda: self.meth("analyze"))
        analButton.pack()
        talkButton = Button(frame, text="talk", background="blue", foreground="black", command=lambda : self.wrapper(motionObj.talk(self.chirp.get())))
        talkButton.pack()
        self.makeChirpEntry()
        self.makeLogPanel()

        pass

    def makeXEntry(self):
        self.moveX = Entry(frame, text="X [-1.0:1.0]")
        self.moveX.pack()
        self.moveX.delete(0, END)
        self.moveX.insert(0, "0.1")
        pass

    def makeYEntry(self):
        self.moveY = Entry(frame, text="Y [-1.0:1.0]")
        self.moveY.pack()
        self.moveY.delete(0, END)
        self.moveY.insert(0, "0")
        pass

    def makeThEntry(self):
        self.moveTh = Entry(frame, text="theta [-1.0:1.0]")
        self.moveTh.pack()
        self.moveTh.delete(0, END)
        self.moveTh.insert(0, "0")
        pass

    def makeFrEntry(self):
        self.moveFr = Entry(frame, text="freq [0.0:1.0]")
        self.moveFr.pack()
        self.moveFr.delete(0, END)
        self.moveFr.insert(0, "0.5")
        pass

    def makeNameEntry(self):
        self.name = Entry(frame)
        self.name.pack()
        self.name.delete(0, END)
        self.name.insert(0, "selfie0")
        pass

    def makeChirpEntry(self):
        self.chirp = Entry(frame)
        self.chirp.pack()
        self.chirp.delete(0, END)
        self.chirp.insert(0, "Gabby is awesome")
        pass

    def makeLogPanel(self):
        self.logPanel = Text(frame, width=400, height=450)
        self.logPanel.insert(END, logObj.getData())
        self.logPanel.pack()
        pass

    def update(self):
        self.logPanel.insert(logObj.getLastEntry())
        pass

    def wrapper(self, fun):
        fun()
        self.update()
        pass


#gui = GUI()
