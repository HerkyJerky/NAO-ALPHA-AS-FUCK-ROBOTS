'''
Created on 7 nov. 2013

@author: Taghi
@author: Dennis
'''

import random
import math
import numpy

PRINT_RESULTS = True

def rand_minus1_plus1():
    """ returns a random number between -1.0 and 1.0 """
    return random.random() * 2.0 - 1.0

class AbstractSLAMProblem:
    
    def __init__(self, world_size = 100.0, measurement_range = 30.0, motion_noise = 1.0, 
                 measurement_noise = 1.0, num_landmarks = 0, initialX = 0, initialY = 0, initialTheta = 0):
        """ Construct an Abstract SLAM Problem world """
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = initialX
        self.y = initialY
        self.theta = initialTheta
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = num_landmarks
        self.make_landmarks(num_landmarks)
        self.true_robot_positions = [[self.x, self.y, self.theta]]
        self.observed_motions = []
        self.observed_measurements = []
        
    def make_landmarks(self, num_landmarks):
        """ Randomly places a given number of landmarks in the world """
        self.landmarks = numpy.zeros((num_landmarks, 2))
        for i in xrange(num_landmarks):
            self.landmarks[i] = [round(rand_minus1_plus1() * self.world_size/2),
                                   round(rand_minus1_plus1() * self.world_size/2)]

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
    
    def run_simulation_dennis(self, num_steps, num_landmarks, world_size, 
                              measurement_range, motion_noise, measurement_noise, distance):
        '''
        At every step, robot will attempt to move distance in whatever direction he's facing
        
        For every 1 unit distance the robot attempts to move, he'll move between -1 and 1 * motion_noise
        extra
        '''
        self.observed_measurements = [None]*num_steps
        
        for i in xrange(num_steps):
            # move robot
            d = distance * (1 + (motion_noise * rand_minus1_plus1()))
            dx = math.cos(self.theta) * d
            dy = math.sin(self.theta) * d
            dtheta = 0
            x = self.x + dx
            y = self.y + dy
            
            if(abs(x) > self.world_size/2 or abs(y) > self.world_size/2):
                '''
                movement determined above would result in moving out of the world
                
                So, instead we turn around 180 degrees, and dont move
                '''
                dtheta = math.pi
                self.theta += dtheta
                self.observed_motions.append([0, 0, 0, 0, dtheta, 0])
            else:
                # execute movement determined above, THEN turn a random amount
                dtheta = rand_minus1_plus1() * math.pi
                self.x += dx
                self.y += dy
                self.theta += dtheta
                self.observed_motions.append([0, 0, d, 0, dtheta, 0])
                
            self.true_robot_positions.append([self.x, self.y, self.theta])
            
            # now figure out landmark measurements
            self.observed_measurements[i] = []
            
            for index in xrange(num_landmarks):
                landmark = self.landmarks[index]
                
                x_lm = landmark[0]
                y_lm = landmark[1]
                
                dx = x_lm - self.x
                dy = y_lm - self.y
                
                dist_to_lm = math.sqrt(dx*dx + dy*dy) * (1 + (measurement_noise * rand_minus1_plus1()))
                        #     actual distance         * (            n o i s e     t e r m            )
                
                if dist_to_lm < measurement_range:
                    rel_angle = math.atan2(dy, dx)
                    self.observed_measurements[i].append([dist_to_lm, rel_angle])
                    
            if(PRINT_RESULTS):
                print "STEP " + str(i) + ": "
                print "    Robot moved " + str(d) + " ahead, and then rotated " + str(dtheta) + " radians."
                
                for index in xrange(len(self.observed_measurements[i])):
                    landmark = self.observed_measurements[i][index]
                    print "    Landmark detected at distance = " + str(landmark[0]) + ", relative angle = " + str(landmark[1])
                
                print ""
                
    
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
    
if __name__ == "__main__":
    num_steps = 10
    num_landmarks = 5
    world_size = 75
    measurement_range = 15
    motion_noise = 0.1
    measurement_noise = 0.1
    distance = 5
    problem = AbstractSLAMProblem(world_size, measurement_range, motion_noise, measurement_noise, num_landmarks)
    problem.run_simulation_dennis(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)