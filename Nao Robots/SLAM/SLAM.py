'''
Created on 8 jan. 2014

@author: Dennis


This is an interface for SLAM classes. For every SLAM algorithm we implement, we
should write a class which extends the class in this file and implements all the methods.

For every SLAM algorithm, we can then when the robot ''launches'' initialize an object,
send data to that SLAM object whenever we measure something, ask it to perform it's
algorithm whenever we like, reset it, etc.

'''

class SLAM:
    
    '''
    Constructor. Perform any initialization here if required.
    '''
    def __init__(self):
        raise NotImplementedError("The constructor of this SLAM algorithms has not yet been implemented!")
    
    '''
    This method should discard all data and previous results and, like the name suggests, reset everything.
    Can use this if things go horribly wrong in some experiment and we want to tweak parameters or something like
    that, and then continue...
    '''
    def reset(self):
        raise NotImplementedError("The reset method of this SLAM algorithm has not yet been implemented!")
    
    '''
    This method should run the SLAM algorithm on all the data it has received so far, and return the results.
    
    If we want to test on-line SLAM, this method will most likely be called again after every time-step, right after
    calling the 2 send_data methods below. If we want to test off-line SLAM, this method will most likely only be called
    a single time
    
    How the algorithm deals with this is up to the specific SLAM implementation. I suppose GraphSLAM will always keep appending
    and memorizing all data forever, and re-run the algorithm from scratch on all data so far, whereas EKF SLAM can discard all
    old data once this method runs and on the next call to this method use the previous results as starting point.
    
    TODO WARNING NOTE IMPORTANT END OF THE WORLD IS IMMINENT IF WE DONT DEAL WITH THIS TAGHI!!!!!
        We should probably precisely describe a single format in which we both return SLAM results. Or did we already do this?
        Either way, we need this so we know exactly what we're returning, in case we want to visualize something or implement
        proper testing functions to analyze results, etc.
    '''
    def run_slam(self):
        raise NotImplementedError("The run_slam method of this SLAM algorithm has not yet been implemented!")
    
    '''
    This method sends an 2D array of measurement-data of a specified time_step to the SLAM algorithm.
    The implementation of the SLAM algorithm will most likely want to append the new data to an internal 
    storage of all data
    
    Expected format of measurement_data:    
    
        A two-dimensional array specific to a single time-step where measurement_data[i] = 
        
            [distance(robot, landmark), relative angle] of the i'th landmark observed at the specified time-step.
            
    This means that if at a certain time-step, 3 different landmarks were observed, measurement_data will be a
    3x2 array (3 arrays each having the 2 elements specified above)
            
    '''
    def send_measurement_data(self, measurement_data, time_step):
        raise NotImplementedError("The send_measurement_data method of this SLAM algorithm has not yet been implemented!")
    
    '''
    This method sends an array of motion-data of a specified time_step to the SLAM algorithm.
    The implementation of the SLAM algorithm will most likely want to append the new
    data to an internal storage of all data
    
    Expected format of motion_data:    [time,action,dForwards,dSideways,dtheta,speed]
    '''
    def send_motion_data(self, motion_data, time_step):
        raise NotImplementedError("The send_motion_data method of this SLAM algorithm has not yet been implemented!")
    
    '''
    This method should set a parameter of a given String parameter_name to a given value.
    
    Currently this seems like easiest way to tweak paremeters without recompiling all the time. We could add
    fields in the GUI to set parameters, and the GUI can call this method.
    
    Will require ugly block of if-else stuff to compare parameter names and set values though... If both
    SLAM algorithms and up having exactly the same set of parameters, we could replace this by a larger number
    of specific set_param_value() methods without string names of parameters, but that won't work (at least not in
    an interface like this) if the two different SLAM algorithms have different sets of parameters
    '''
    def set_parameter(self, parameter_name, value):
        raise NotImplementedError("The set_paramter method of this SLAM algorithm has not yet been implemented!")