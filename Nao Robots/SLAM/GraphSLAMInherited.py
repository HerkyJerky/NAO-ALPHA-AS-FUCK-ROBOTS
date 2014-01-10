'''
Created on 9 Jan 2014

@author: Taghi
'''
import SLAM
import GraphSLAM
import CommonFunctionality

class GraphSLAMInherited(SLAM):
    
    def __init__(self):
        print "Graph Slam is initialized!"
        '''
        This is an graph slam object that will be the main engine for this class.
        '''
        self.graphSlam = GraphSLAM()
        self.motions = []
        self.measurements = []
        self.motion_noise = 1
        self.measurement_noise = 1
    
    def reset(self):
        print "Reseting GraphSLAM!"
        # I think that is what I have to do with reset method? Just initialize it from zero?
        self.graphSlam = GraphSLAM() 
        
    def run_slam(self):
        print "Running graph slam!"
        engine = CommonFunctionality()
        data = engine.make_data(self.motions,self.measurements)
        result = self.graphSlam.graphSlam(None,data,len(data) + 1,len(engine.landmarks),self.motion_noise,self.measurement_noise)
        motion_approximations = []
        landmarks_approximations = []
        for k in range(len(self.motions)):
            motion_approximations.append([result[2*k],result[2*k+1]])
            
        for i in range(len(engine.landmarks)):
            landmarks_approximations.append([result[2*(len(self.motions)+i)],result[2*(len(self.motions)+i) + 1]])
            
        return [motion_approximations,landmarks_approximations]   
    
    def send_data(self,measurement_data,motion_data):
        self.measurements.append(measurement_data)
        self.motions.append(motion_data) 
        
    def set_parameter(self,parameter_name,value):
        print "Setting some parameter for graph slam!"
        # TODO : Not sure about this part.
    