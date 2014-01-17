__author__ = 'redsphinx'

#from NAOControl import NAOControl
from Motion import Motion
from Vision import Vision
#from EkfSLAM import EkfSLAM
#from GraphSLAMInherited import GraphSLAMInherited
#from ImageProcessing import ImageProcessing
#from MapViewer import MapViewer
from AnalyseImage import AnalyseImage

analyzeObj = AnalyseImage()
motionObj = Motion()
visionObj = Vision()
#ekfSlamObj = EkfSLAM()
#graphSlamObj = GraphSLAMInherited()
#imageProcObj = ImageProcessing()
#mapViewer = MapViewer()
TYPES = ["EKF", "GRAPH"]
MODES = ["ONLINE", "OFFLINE"]

'''
1. LET robot walk around and then take pictures
2. DO image processing
3. SEND data for slam
4. RUN slam
if online:
    5. DISPLAY map
    6. GO to step 1
    repeat until we decide to stop
elif offline
    at step 3, go to step 1
    repeat until a certain iteration has been reached
    4. RUN slam
    5. DISPLAY map
'''

# TODO fix the output to interpret matrix form

class ControlFlow:
    def __init__(self):
        #ekfSlamObj.set_noise_parameters(0.1, 0.1, 0.1)
        #graphSlamObj.set_noise_parameters(1, 1, 1)
        pass

    def testImage(self):
        self.angle = visionObj.takePic()
        print "image taken"
        print self.part_2()

    def flow_online(self):
        cntr = 0
        while True:
            #1. LET robot walk around and then take pictures
            # move 20 cm forward
            if cntr % 2 == 0:
                motion_data = self.part_1(20, 0, 0)
            else:
                # turn 90 deg clockwise
                motion_data = self.part_1(0, 0, 90)
            #2. DO image processing
            measurement_data = self.part_2()
            #3. SEND data for slam, Ekf
            self.part_3(measurement_data, motion_data, TYPES[0])
            #4. RUN slam
            dataForMap = self.part_4(TYPES[0])
            #5. DISPLAY map
            self.part_5(dataForMap)
            #6. GO to step 1
            cntr += 1
            print cntr
            if cntr == 10:
                break

    def flow_offline(self):
        cntr = 0
        while True:
            #1. LET robot walk around and then take pictures
            # move 20 cm forward
            if cntr % 2 == 0:
                motion_data = self.part_1(20, 0, 0)
            else:
                # turn 90 deg clockwise
                motion_data = self.part_1(0, 0, 90)
            #2. DO image processing
            measurement_data = self.part_2()
            #3. SEND data for slam, Graph
            self.part_3(measurement_data, motion_data, TYPES[1])
            #4. RUN slam
            dataForMap = self.part_4(TYPES[1])
            #6. GO to step 1
            cntr += 1
            print cntr
            if cntr == 10:
                #5. DISPLAY map
                self.part_5(dataForMap)
                break


    # 1. LET robot walk around and then take pictures
    def part_1(self, x, y, theta):
        print "part 1 initializing"
        if theta == 0:
            motion_data = motionObj.moveXYCm(x, y)
            visionObj.takePic()
        elif x and y == 0:
            motion_data = motionObj.rotateTheta(theta)
            self.angle = visionObj.takePic()
        print "part 1 COMPLETE"
        return motion_data

    # 2. DO image processing
    def part_2(self):
        print "part 2 initializing"
        measurement_data = analyzeObj.analyse("analyzeThis.png", self.angle)
        print "part 2 COMPLETE"
        return measurement_data

    # 3. SEND data for slam
    def part_3(self, measurement_data, motion_data, kind):
        print "part 3 initializing"
        if kind == TYPES[0]:
            ekfSlamObj.send_data(measurement_data, motion_data)
        elif kind == TYPES[1]:
            graphSlamObj.send_data(measurement_data, motion_data)
        print "part 3 COMPLETE"

    # 4. RUN slam
    def part_4(self, kind):
        print "part 4 initializing"
        if kind == TYPES[0]:
            dataForMap = ekfSlamObj.run_slam()
        elif kind == TYPES[1]:
            dataForMap = graphSlamObj.run_slam()
        print "part 4 COMPLETE"
        return dataForMap

    def part_5(self, dataForMap):
        mapViewer.updateMap(dataForMap)

        # TODO finish this

controlThisShit = ControlFlow()
print "control flow made"
#controlThisShit.flow_online()

controlThisShit.testImage()