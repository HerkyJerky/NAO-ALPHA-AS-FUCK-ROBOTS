'''
Created on 9 Oct 2013

@author: Taghi
'''
import numpy as np
import random
import math as MH

class actualSlam:
    
    def __init__(self, world_size = 100.0, measurement_range = 30.0,
                 motion_noise = 1.0, measurement_noise = 1.0):
        self.measurement_noise = 0.0
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = 0
        
    def make_landmarks(self, num_landmarks):
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append([round(random.random() * self.world_size),
                                   round(random.random() * self.world_size)])
        self.num_landmarks = num_landmarks
        
        
    def move(self, dx, dy):

        x = self.x + dx + self.rand() * self.motion_noise
        y = self.y + dy + self.rand() * self.motion_noise

        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True
    

    def sense(self):
        Z = []
        for i in range(self.num_landmarks):
            dx = self.landmarks[i][0] - self.x + self.rand() * self.measurement_noise
            dy = self.landmarks[i][1] - self.y + self.rand() * self.measurement_noise    
            if self.measurement_range < 0.0 or abs(dx) + abs(dy) <= self.measurement_range:
                Z.append([i, dx, dy])
        return Z
    
    def rand(self):
        return random.random() * 2.0 - 1.0

def slam(data,N,num_landmarks, motion_noise, measurement_noise, initialX, initialY):
    dim = 2*(N + num_landmarks)
    
    
    Omega = np.zeros((dim,dim))
    #Omega = np.zeros((dim,dim))
    Omega[0,0] = 1.0
    Omega[1,1] = 1.0
    
    Xi = np.zeros((dim,1))
    Xi[0,0] = initialX
    Xi[1,0] = initialY
    
    # Have you ever seen watchmen asked me Gabi at this point
    
    # This loop is just for motions. Measurements might be easily added to data array and it is good to go bitches
    for k in range(len(data)):
        n = k * 2
        measurement = data[k][0]
        motion = data[k][1]
        for i in range(len(measurement)):
            m = 2 * (N + measurement[i][0])
            
            for b in range(2):
                Omega[n+b][n+b] = Omega[n+b][n+b] + 1.0/measurement_noise
                Omega[m+b][m+b] = Omega[m+b][m+b] + 1.0/measurement_noise
                Omega[n+b][m+b] = Omega[n+b][m+b] - 1.0/measurement_noise
                Omega[m+b][n+b] = Omega[m+b][n+b] - 1.0/measurement_noise
                Xi[n+b][0] = Xi[n+b][0] - measurement[i][1+b] / measurement_noise
                Xi[m+b][0] = Xi[m+b][0] + measurement[i][1+b] / measurement_noise
                
        for b in range(4):
            Omega[n+b][n+b] = Omega[n+b][n+b] + 1.0/motion_noise
        for b in range(2):
            Omega[n+b][n+b+2] += -1.0/motion_noise
            Omega[n+b+2][n+b] += -1.0/motion_noise
            Xi[n+b][0] += -motion[b] / motion_noise
            Xi[n+b+2][0] += motion[b]/motion_noise
 
    #print np.size(Omega, 0)
    #print np.size(Omega, 1)
    invOmega = np.linalg.inv(Omega)
    
    #invOmega = np.linalg.cholesky(Omega)
    #Omega = np.linalg.pinv(invOmega)
    mu = np.dot(invOmega,Xi)
    
    
    return mu
    #return 1   
       
def make_data(N, num_landmarks, world_size, measurement_range, motion_noise, 
              measurement_noise, distance):

    complete = False

    while not complete:

        data = []

        # make robot and landmarks
        r = actualSlam(world_size, measurement_range, motion_noise, measurement_noise)
        r.make_landmarks(num_landmarks)
        seen = [False for row in range(num_landmarks)]
    
        # guess an initial motion
        orientation = random.random() * 2.0 * MH.pi
        dx = MH.cos(orientation) * distance
        dy = MH.sin(orientation) * distance
    
        for k in range(N-1):
    
            # sense
            Z = r.sense()

            # check off all landmarks that were observed 
            for i in range(len(Z)):
                seen[Z[i][0]] = True
    
            # move
            while not r.move(dx, dy):
                # if we'd be leaving the robot world, pick instead a new direction
                orientation = random.random() * 2.0 * MH.pi
                dx = MH.cos(orientation) * distance
                dy = MH.sin(orientation) * distance

            # memorize data
            data.append([Z, [dx, dy]])

        # we are done when all landmarks were observed; otherwise re-run
        complete = (sum(seen) == num_landmarks)

    print ' '
    print 'Landmarks: ', r.landmarks
    print r

    return data       
  
  
def print_result(N, num_landmarks, result):
    print
    print 'Estimated Pose(s):'
    for i in range(N):
        print '    ['+ ', '.join('%.3f'%x for x in result[2*i]) + ', ' \
            + ', '.join('%.3f'%x for x in result[2*i+1]) +']'
    print 
    print 'Estimated Landmarks:'
    for i in range(num_landmarks):
        print '    ['+ ', '.join('%.3f'%x for x in result[2*(N+i)]) + ', ' \
            + ', '.join('%.3f'%x for x in result[2*(N+i)+1]) +']'
                   
'''
This is the test case. I will just assume some numbers to check if it actually works
'''        
if __name__ == "__main__":
    import sys
    N = 2
    world_size = 100.0
    measurement_range = 50.0
    distance = 3.0
    num_landmarks = 0
    measurement_noise = 1.0
    motion_noise = 1.0
    data = make_data(N,num_landmarks,world_size,measurement_range,motion_noise,measurement_noise,distance)
    a = slam(data,N,num_landmarks,motion_noise,measurement_noise, 50.0, 50.0)
    print_result(N,num_landmarks, a)
    
    
    
    