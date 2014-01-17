'''
Created on 9 Jan 2014

@author: Taghi
'''
import SLAM
import GraphSLAM
import CommonFunctionality

class GraphSLAMInherited(SLAM):
    
    def __init__(self):
        '''
        This is an graph slam object that will be the main engine for this class.
        '''
        self.graphSlam = GraphSLAM()
        self.motions = []
        self.measurements = []
        self.motion_noise = 1
        self.measurement_noise = 1
        self.associationError = 0.25
        self.method = True
        print "Graph Slam is initialized!"
    
    def reset(self):
        print "Reseting GraphSLAM!"
        # I think that is what I have to do with reset method? Just initialize it from zero?
        self.graphSlam = GraphSLAM() 
        self.motions = []
        self.measurements = []
        self.motion_noise = 1
        self.measurement_noise = 1
        self.associationError = 0.25
        self.method = True
        print "Reseting done!"
        
    def run_slam(self):
        # TODO : Needs to be tested somehow.
        print "Running graph slam!"
        engine = CommonFunctionality(self.associationError)
        data = engine.make_data(self.motions,self.measurements)
        result = self.graphSlam.graphSlam(None,data,len(data) + 1,len(engine.landmarks),self.motion_noise,self.measurement_noise)
        motion_approximations = []
        landmarks_approximations = []
        # Getting all the results.
        # One thing to clear up : data[k] goes into the k-th time step. data[k][1] goes into motion data. 
        # [0] is strange thing but you have to do it. 
        # [2] is index of orientation at that time step.
        if (self.method):
            for k in range(len(self.motions)):
                motion_approximations.append([result[2*k],result[2*k+1],data[k][1][0][2]])
                
            for i in range(len(engine.landmarks)):
                landmarks_approximations.append([result[2*(len(self.motions)+i)],result[2*(len(self.motions)+i) + 1]])
        
        # Getting only last elements
        if (self.method == False):
            lengthOfMotion = len(self.motions)
            motion_approximations.append([result[2*lengthOfMotion],result[2*lengthOfMotion+1],data[lengthOfMotion - 1][1][0][2]])
            for i in range(len(engine.landmarks)):
                landmarks_approximations.append([result[2*(len(self.motions)+i)],result[2*(len(self.motions)+i) + 1]])
        
        # Returning results depending on what method is used. Return statement does not change only the way matrices are generated 
        print "Graph SLAM is done!"  
        return [motion_approximations,landmarks_approximations]   
    
    def send_data(self,measurement_data,motion_data):
        self.measurements.append(measurement_data)
        self.motions.append(motion_data) 
        
    def set_parameter(self,parameter_name,value):
        print "Setting some parameter for graph slam!"
        # TODO : Not sure about this part.
        
    def set_noise_parameters(self,measurement_noise_range,measurement_noise_bearing,motion_noise):
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise_bearing
        
    def set_offline(self):
        self.method = False
    