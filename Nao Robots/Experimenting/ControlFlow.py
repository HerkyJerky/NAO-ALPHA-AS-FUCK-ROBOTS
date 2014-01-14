__author__ = 'redsphinx'

from NAOControl import NAOControl
from Motion import Motion
from Vision import Vision
from EkfSLAM import EkfSLAM
from GraphSLAMInherited import GraphSLAMInherited
from ImageProcessing import ImageProcessing
from MapViewer import MapViewer

motionObj = Motion()
visionObj = Vision()
ekfSlamObj = EkfSLAM()
graphSlamObj = GraphSLAMInherited()
imageProcObj = ImageProcessing()
mapViewer = MapViewer()
TYPES = ["EKF", "GRAPH"]
MODES = ["ONLINE", "OFFLINE"]


class ControlFlow:
    def __init__(self):
        ekfSlamObj.set_noise_parameters(0.1, 0.1, 0.1)
        graphSlamObj.set_noise_parameters(1, 1, 1)

    def flow(self):
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
        pass

    # 1. LET robot walk around and then take pictures
    def part_1(self, x, y, theta):
        print "part 1 initializing"
        if theta == 0:
            motion_data = motionObj.moveXYCm(x, y)
            visionObj.takePic()
        elif x and y == 0:
            motion_data = motionObj.rotateTheta(theta)
            visionObj.takePic()
        print "part 1 COMPLETE"
        return motion_data

    # 2. DO image processing
    def part_2(self):
        print "part 2 initializing"
        measurement_data = imageProcObj.getClusterPoints()  # TODO fix, this is not correct
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
