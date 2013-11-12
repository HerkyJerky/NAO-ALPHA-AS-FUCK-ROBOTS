'''
Created on 7 nov. 2013

@author: Taghi
@author: Dennis
'''
     
from AbstractSLAMProblem import *;
import numpy

def graphSlam(data, N, num_landmarks, motion_noise, measurement_noise, initialX, initialY):
    dim = 2*(N + num_landmarks)
    
    Omega = numpy.zeros((dim,dim))
    #Omega = np.zeros((dim,dim))
    Omega[0,0] = 1.0
    Omega[1,1] = 1.0
    
    Xi = numpy.zeros((dim,1))
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
    invOmega = numpy.linalg.inv(Omega)
    
    #invOmega = np.linalg.cholesky(Omega)
    #Omega = np.linalg.pinv(invOmega)
    mu = numpy.dot(invOmega,Xi)
    
    return mu

def print_result(num_steps, num_landmarks, result):
    print
    print 'Estimated Pose(s):'
    for i in range(num_steps):
        print '    ['+ ', '.join('%.3f'%x for x in result[2*i]) + ', ' \
            + ', '.join('%.3f'%x for x in result[2*i+1]) +']'
    print 
    print 'Estimated Landmarks:'
    for i in range(num_landmarks):
        print '    ['+ ', '.join('%.3f'%x for x in result[2*(num_steps+i)]) + ', ' \
            + ', '.join('%.3f'%x for x in result[2*(num_steps+i)+1]) +']'
  
'''
This is the test case. I will just assume some numbers to check if it actually works
''' 
if __name__ == "__main__":
    numSteps = 3
    world_size = 100.0
    measurement_range = 50.0
    walkingDistancePerStep = 3.0
    num_landmarks = 2
    measurement_noise = 1.0
    motion_noise = 1.0
    
    problem = AbstractSLAMProblem(world_size, measurement_range, motion_noise, measurement_noise, num_landmarks);
    data = problem.run_simulation(numSteps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, walkingDistancePerStep);
    mu = graphSlam(data, numSteps, num_landmarks, motion_noise, measurement_noise, 50.0, 50.0)
    print_result(numSteps,num_landmarks, mu)