'''
Created on 7 nov. 2013

@author: Taghi
@author: Dennis
'''

import random
import math

class AbstractSLAMProblem:
    
    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0, num_landmarks = 0, initialX = 0, initialY = 0):
        """ Construct an Abstract SLAM Problem world """
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = initialX
        self.y = initialY
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = num_landmarks
        self.make_landmarks(num_landmarks)
        
    def make_landmarks(self, num_landmarks):
        """ Randomly places a given number of landmarks in the world """
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
        self.num_landmarks = num_landmarks
        
    def moveRobot(self, dx, dy):
        """ 
        Attempts to move the robot dx and dy away from it's current location. 
        Motion_noise can increase or decrease the true distance travelled
        
        Returns false if movement would result in moving out of the world
        """

        x = self.x + dx + self.rand_minus1_plus1() * self.motion_noise
        y = self.y + dy + self.rand_minus1_plus1() * self.motion_noise

        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True

    def sense(self):
        """
        Returns an array of vision measurements, affected by measurement_noise.
        
        The array contains an array of 3 elements for each landmark observed: [i, dx, dy] where
        i = index of the observed landmark
        dx = x_landmark - x_robot + noise
        dy = y_landmark - y_robot + noise
        
        """
        
        Z = []
        for i in range(self.num_landmarks):
            dx = self.landmarks[i][0] - self.x + self.rand_minus1_plus1() * self.measurement_noise
            dy = self.landmarks[i][1] - self.y + self.rand_minus1_plus1() * self.measurement_noise    
            if self.measurement_range < 0.0 or abs(dx) + abs(dy) <= self.measurement_range:
                Z.append([i, dx, dy])
        return Z
    
    def rand_minus1_plus1(self):
        """ returns a random number between -1.0 and 1.0 """
        return random.random() * 2.0 - 1.0
    
    def run_simulation(self, num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance):
        """
        Runs a full simulation of a robot moving through the map, and returns the data gathered
        throughout the entire simulation.
        
        So, how the data actually looks like (Sorry for delay Dennis, I know it is very much of a mind fuck going on here)
        
        First, I will try to explain with words what is happening : 
        - So, data is assumed to be big matrix saving all data( this might have down side but whatever). It takes number of steps simulation
        had and loops through. dx and dy are movement towards x and y direction each time step.
        - Each time step we sense around to see if we see some landmark and we "move" towards where we should be moving
        - After those are done we end up with some sense array and new coordinate of where we "are"
        - Data array keeps those stuff depending on time step. So if you need data from time step t you access data[t]
        - To access sense of data[t] you call data[t][0]
        - To access coordinate at time step t you call data[t][1]
        - This might lead to some issues maybe especially on fact that Z might be empty at some points but that will be checked
        by make data method probably and in slam if it is empty then we do not append anything to slam Matrix(omega)
        
        """
        data = []
        
        # guess an initial motion
        orientation = random.random() * 2.0 * math.pi
        dx = math.cos(orientation) * distance
        dy = math.sin(orientation) * distance
        
        for k in range(num_steps - 1):
        
            # sense
            Z = self.sense()
        
            # move
            while not self.moveRobot(dx, dy):
                # if we'd be leaving the robot world, pick instead a new direction
                orientation = random.random() * 2.0 * math.pi
                dx = math.cos(orientation) * distance
                dy = math.sin(orientation) * distance
    
            # memorize data
            data.append([Z, [dx, dy]])
    
        print ' '
        print 'Landmarks: ', self.landmarks
        print self
    
        return data  
    
    def make_data(self,motion_array,measurement_array):
        '''
        This method is same as run_simulation but points are not random. I get data from Roel and others and put it in data
        array which is used by graph slam algo. Structure of array is same as before. But I will try to think of some way
        to deal with non square array thing. Idea is that, size of data array is size of motion array but we also append
        landmarks to it. So, if we haven`t seen anything at that moment, we won`t update our matrix with any data about landmarks
        but motion will still be updated. So, to summarize, every element of data is one whole step of motion and measurements.
        As already mentioned at time step t, motion at t is data[t][1] and measurements of time step t is data[t][0]
        '''
        data = []
        
        # We do not need any randomness, so we will just go through arrays and add data
        
        numSteps = len(motion_array)
        
        # This part should be clarified, because I am not sure how data is going to be send around
        # My assumption : measurement_array has measurement send from Roel but we update that array with newer one before sending it here where indices are specified as well
        # For motion I assume it is an array that has dx and dy in it. Some preprocessing might be needed
        # Preprocessing needed might be about addind data send by Gabi to history of motions in case Gabi sends only last motion.
        
        # For now this method just loops through two arrays and appends them in a way that was done before.
        # This might need some altering.
        
        for k in range(numSteps):
            
            data.append([measurement_array[k],motion_array[k]])
            
        return data
            
        
        