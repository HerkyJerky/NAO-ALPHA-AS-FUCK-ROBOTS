__author__ = 'redsphinx'

# since this class is pretty empty and useless, I will explain the structure here:
# we have a class for all main parts of the project:
# -> Vision         Everything vision related, Roel's code should go here
# -> SlamStuff      Everything SLAM related, Taghi's and Dennis' code should go here
# -> Motion         Everything motion related. Right now to keep it simple, we only move the entire body as one
# -> Logger         Everything to do with saving and retrieving the data we need
# they all come together in the class GUI which functions like a controller for the NAO


#from SuperGUI import SuperGUI
#from MapControl import  MapGUI
from NAOControl import NAOControl


#gui = GUI()
naoControl = NAOControl()

