__author__ = 'redsphinx'

#from NAOControl import NAOControl
from Motions import Motion
from Vision import Vision
from EkfSLAM import EkfSLAM
from GraphSLAMInherited import GraphSLAMInherited
#from ImageProcessing import ImageProcessing
#from MapViewer import MapViewer
from AnalyseImage import AnalyseImage

analyzeObj = AnalyseImage()
motionObj = Motion()
visionObj = Vision()
ekfSlamObj = EkfSLAM()
graphSlamObj = GraphSLAMInherited()
#imageProcObj = ImageProcessing()
#mapViewer = MapViewer()
TYPES = ["EKF", "GRAPH"]
MODES = ["ONLINE", "OFFLINE"]
# TODO be able to set ip and port in here and not in Vision and Motions
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


class ControlFlow:
    def __init__(self):
        ekfSlamObj.set_noise_parameters(0.1, 0.1, 0.1)
        #graphSlamObj.set_noise_parameters(1, 1, 1)
        # theta from output SLAM must be in radians
        pass

    def testImage(self):
        self.angle, self.cameraHeight = visionObj.takePic()
        print "image taken"
        print self.part_2()

    def flow_online(self, kind):
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
            self.part_3(measurement_data, motion_data, kind)
            #4. RUN slam
            dataForMap = self.part_4_online(kind)
            print dataForMap
            #5. DISPLAY map
            #self.part_5(dataForMap)
            #6. GO to step 1
            cntr += 1
            print cntr
            if cntr == 10:
                break

    def flow_offline(self, kind):
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
            self.part_3(measurement_data, motion_data, kind)
            #4. RUN slam
            dataForMap = self.part_4_offline(kind)
            print dataForMap
            #6. GO to step 1
            cntr += 1
            print cntr
            if cntr == 10:
                #5. DISPLAY map
                #self.part_5(dataForMap)
                break


    # 1. LET robot walk around and then take pictures
    def part_1(self, x, y, theta):
        print "part 1 initializing - walk and take pic"
        if theta == 0:
            motion_data = motionObj.moveXYCm(x, y)
            print 'we have motiondata: ', motion_data
            self.angle, self.cameraHeight = visionObj.takePic()
        elif ((x == 0) and (y == 0)):
            motion_data = motionObj.rotateTheta(theta)
            self.angle, self.cameraHeight = visionObj.takePic()
            print 'we have motiondata2: ', motion_data
        else:
            print 'no valid x y or theta'

        print "part 1 COMPLETE"
        return motion_data

    # 2. DO image processing
    def part_2(self):
        print "part 2 initializing - process the image"
        measurement_data = analyzeObj.analyse("analyzeThis.png", self.angle, self.cameraHeight)
        print "part 2 COMPLETE"

        return measurement_data

    # 3. SEND data for slam
    def part_3(self, measurement_data, motion_data, kind):
        print "part 3 initializing - send data for SLAM"
        print 'measurement_date = ', measurement_data
        if kind == TYPES[0]:
            ekfSlamObj.send_data(measurement_data, motion_data)
        elif kind == TYPES[1]:
            graphSlamObj.send_data(measurement_data, motion_data)
        print "part 3 COMPLETE"

    # 4. RUN slam
    def part_4_online(self, kind):
        print "part 4 initializing - run SLAM"
        if kind == TYPES[0]:
            dataForMap = ekfSlamObj.run_slam()
        elif kind == TYPES[1]:
            dataForMap = graphSlamObj.run_slam()
        print "part 4 COMPLETE"
        return dataForMap

    def part_4_offline(self, kind):
        print "part 4 initializing - run SLAM"
        if kind == TYPES[0]:
            ekfSlamObj.set_offline()
            dataForMap = ekfSlamObj.run_slam()
        elif kind == TYPES[1]:
            graphSlamObj.set_offline()
            dataForMap = graphSlamObj.run_slam()
        print "part 4 COMPLETE"
        return dataForMap

    def part_5(self, dataForMap):
        #mapViewer.mapSLAM(dataForMap)
        pass


controlThisShit = ControlFlow()
#print "control flow made"
#controlThisShit.flow_online()
# TYPES = ["EKF", "GRAPH"]
#controlThisShit.flow_online(TYPES[0])
#controlThisShit.flow_offline(TYPES[1])
controlThisShit.flow_offline(TYPES[1])

#controlThisShit.testImage()