__author__ = 'redsphinx'

from cv2.cv import *


img = LoadImage("/home/USER/Pictures/python.jpg")
NamedWindow("opencv")
ShowImage("opencv",img)
WaitKey(0)./opencv_test_corey



#class Thing:
#    def __init__(self):
#        pass
#
#    def twoValues(self):
#        return 5, 4, 8, 7
#
#    def receive(self):
#        a, b, c, d = self.twoValues()
#        print a
#        print b
#        print c
#        print d
#
#    def moreVars(self):
#        a, b = 3
#        print a
#        print b
#        #print c

thing = Thing()
thing.receive()
thing.moreVars()
#from Tkinter import Tk, Canvas, Frame, BOTH
#
#
#class Example(Frame):
#
#    def __init__(self, parent):
#        Frame.__init__(self, parent)
#
#        self.parent = parent
#        self.initUI()
#
#    def initUI(self):
#
#        self.parent.title("Colors")
#        self.pack(fill=BOTH, expand=1)
#
#        canvas = Canvas(self)
#        canvas.create_rectangle(20, 30, 25, 35,
#            outline="#fb0", fill="#fb0")
#        canvas.create_rectangle(150, 10, 240, 80,
#            outline="#f50", fill="#f50")
#        canvas.create_rectangle(270, 10, 370, 80,
#            outline="#05f", fill="#05f")
#        canvas.pack(fill=BOTH, expand=1)
#
#
#def main():
#
#    root = Tk()
#    ex = Example(root)
#    root.geometry("400x100+300+300")
#    root.mainloop()
#
#
#if __name__ == '__main__':
#    main()


#from Tkinter import *
#
#class Application(Frame):
#    def __init__(self, master=None):
#        Frame.__init__(self, master)
#        self.parent = master
#        self.initUI()
#
#    def initUI(self):
#        self.outputBox = Text(self.parent, bg='yellow', height= 10, fg='green', relief=SUNKEN, yscrollcommand='TRUE')
#        self.outputBox.pack(fill='both', expand=True)
#        self.button1 = Button(self.parent, text='button1', width=20, bg ='blue', fg='green', activebackground='black', activeforeground='green')
#        self.button1.pack(side=RIGHT, padx=5, pady=5)
#        self.button2 = Button(self.parent, text='button2', width=25, bg='white', fg='green', activebackground='black', activeforeground='green')
#        self.button2.pack(side=LEFT, padx=5, pady=5)
#
#def main():
#    root = Tk()
#    app = Application(root)
#    app.parent.geometry('300x200+100+100')
#    app.parent.configure(background = 'red')
#    app.mainloop()
#
#main()