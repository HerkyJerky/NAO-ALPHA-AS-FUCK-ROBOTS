'''
Created on 7 nov. 2013

@author: Taghi
@author: Dennis
'''

import random
import math

class AbstractSLAMProblem:
    
    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0, num_landmarks = 0):
        """ Construct an Abstract SLAM Problem world """
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
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