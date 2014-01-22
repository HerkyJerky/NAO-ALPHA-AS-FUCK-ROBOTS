'''
Created on 9 Jan 2014

@author: Taghi
'''
import SLAM
from GraphSLAM import GraphSLAM
import numpy as np
from CommonFunctionality import CommonFunctionality

class GraphSLAMInherited(SLAM.SLAM):
    
    def __init__(self):
        '''
        This is an graph slam object that will be the main engine for this class.
        '''
        self.graphSlam = GraphSLAM()
        self.motions = []
        self.measurements = []
        self.motion_noise = 2.0
        self.measurement_noise = 2.0
        self.associationError = 400
        self.method = True
        print "Graph Slam is initialized!"
    
    def reset(self):
        print "Reseting GraphSLAM!"
        # I think that is what I have to do with reset method? Just initialize it from zero?
        self.graphSlam = GraphSLAM() 
        self.motions = []
        self.measurements = []
        self.motion_noise = 2.0
        self.measurement_noise = 2.0
        self.associationError = 400
        self.method = True
        print "Reseting done!"
        
    def run_slam(self):
        # TODO : Needs to be tested somehow.
        print "Running graph slam!"
        engine = CommonFunctionality(self.associationError)
        data = engine.make_data(self.motions,self.measurements)
        [result,booleans] = self.graphSlam.graphSlam(data,len(data) + 1,len(engine.landmarks),self.motion_noise,self.measurement_noise)
        # Getting all the results.
        # One thing to clear up : data[k] goes into the k-th time step. data[k][1] goes into motion data. 
        # [0] is strange thing but you have to do it. 
        # [2] is index of orientation at that time step.
        if (self.method == False):
            motion_approximations = np.zeros((len(self.motions) + 1,3))
            landmarks_approximations = np.zeros((len(engine.landmarks),3))
            for k in range(len(self.motions) + 1):
                motion_approximations[k][0] = result[2*(k)]
                motion_approximations[k][1] = result[2*(k)+1]
                if (k>0):
                    motion_approximations[k][2] = data[k-1][1][0][2]
                else:
                    motion_approximations[k][2] = 0.0
                #motion_approximations.append([result[2*k],result[2*k+1],data[k][1][0][2]])
                
            for i in range(len(engine.landmarks)):
                landmarks_approximations[i][0] = result[2*(len(self.motions) + i)]
                landmarks_approximations[i][1] = result[2*(len(self.motions) + i) + 1]
                #print booleans[i]
                landmarks_approximations[i][2] = booleans[i]
                #landmarks_approximations.append([result[2*(len(self.motions)+i)],result[2*(len(self.motions)+i) + 1]])
        
        # Getting only last elements
        if (self.method == True):
            motion_approximations = np.zeros((1,3))
            landmarks_approximations = np.zeros((len(engine.landmarks),3))

            motion_approximations[0][0] = result[2*len(self.motions)]
            motion_approximations[0][1] = result[2*len(self.motions) + 1]
            motion_approximations[0][2] = data[len(self.motions) - 1][1][0][2]

            for i in range(len(engine.landmarks)):
                landmarks_approximations[i][0] = result[2*(len(self.motions) + i)]
                landmarks_approximations[i][1] = result[2*(len(self.motions) + i) + 1]
                #print booleans[i]
                landmarks_approximations[i][2] = booleans[i]
        
        # Returning results depending on what method is used. Return statement does not change only the way matrices are generated 
        print "Graph SLAM is done!"
        #return result
        return np.array([motion_approximations,landmarks_approximations])
    
    def send_data(self,measurement_data,motion_data):
        self.measurements.append(measurement_data)
        self.motions.append(motion_data) 
        
    def set_parameter(self,parameter_name,value):
        print "Setting some parameter for graph slam!"
        # TODO : Not sure about this part.
        
    def set_noise_parameters(self,measurement_noise_range,measurement_noise_bearing,motion_noise):
        self.motion_noise = 2.0
        self.measurement_noise = 2.0
        
    def set_offline(self):
        self.method = False
    