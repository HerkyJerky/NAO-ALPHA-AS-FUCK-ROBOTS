'''
Created on 7 nov. 2013

@author: Taghi
@author: Dennis
'''
     
from AbstractSLAMProblem import *
from CommonFunctionality import *
import numpy

def graphSlam(data, N, num_landmarks_seen, motion_noise, measurement_noise, initialX = 0, initialY = 0):
    #dim = 2*(N + num_landmarks)
    
    # Initialize 2x2 zeros matrix to start with. Meaning one motion?
    # Afterwards we have to append stuff to matrix. We can not assume that we will see landmarks all the time
    # Also, idea : We can make use of data for dim
    dim = 2 * (N + num_landmarks_seen)
    
    #Omega = numpy.zeros(2,2)
    Omega = numpy.zeros((dim,dim))
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
        motion = data[k][1][0]
        for i in range(len(measurement)):
            one_measurement = measurement[i]
            # Check if we have actually seen something there and if there is something to read at all.
            # This should fix issue we had before with graph slam.
            if (len(one_measurement)!=0):
                m = 2 * (N + one_measurement[0])
                
                for b in range(2):
                    Omega[n+b][n+b] = Omega[n+b][n+b] + 1.0/measurement_noise
                    Omega[m+b][m+b] = Omega[m+b][m+b] + 1.0/measurement_noise
                    Omega[n+b][m+b] = Omega[n+b][m+b] - 1.0/measurement_noise
                    Omega[m+b][n+b] = Omega[m+b][n+b] - 1.0/measurement_noise
                    Xi[n+b][0] = Xi[n+b][0] - one_measurement[1+b] / measurement_noise
                    Xi[m+b][0] = Xi[m+b][0] + one_measurement[1+b] / measurement_noise
                
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
            
            
def slam_experiment(num_steps, num_landmarks, world_size, 
                              measurement_range, motion_noise, measurement_noise, distance):
    # For now, I am asking for exactly the parameters that run_simulation_dennis method needs + world_size
    simulation = AbstractSLAMProblem(world_size, measurement_range, motion_noise, measurement_noise, num_landmarks)  
    # running the simulation
    simulation.run_simulation_dennis(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance) 
    # Reading data after simulation
    gabi_array = simulation.observed_motions
    roel_array = simulation.observed_measurements
    
    engine = CommonFunctionality()
    data = engine.make_data(gabi_array,roel_array)
    
    calculation_motion_noise = 2.0
    calculation_measurement_noise = 2.0
    mu = graphSlam(data,len(data),len(engine.landmark),calculation_motion_noise,calculation_measurement_noise)
    
    print_result(len(data),len(engine.landmarks),mu)       
'''
This is the test case. I will just assume some numbers to check if it actually works
''' 
if __name__ == "__main__":
    #numSteps = 3
    world_size = 100.0
    measurement_range = 50.0
    walkingDistancePerStep = 3.0
    num_landmarks = 0
    measurement_noise = 1.0
    motion_noise = 1.0
    
    #problem = AbstractSLAMProblem(world_size, measurement_range, motion_noise, measurement_noise, num_landmarks)
    engine = CommonFunctionality()
    # Moves 2 towards x, 2 towards y, turn 45 degrees and goes 4 towards x in that direction.
    gabi_array = [[0,3,2,0,0,10],[1,3,0,2,0,10],[1,3,3,0,0,10],[1,3,0,0,0,10]] 
    # Structure of roel array : [d(r,l),relAngle] of landmarks seen at time step t.
    roel_array = [[],[],[],[]]
    #data = problem.run_simulation(numSteps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, walkingDistancePerStep);
    data = engine.make_data(gabi_array, roel_array)
    #numSteps = len(data)
    mu = graphSlam(data, len(data) + 1, len(engine.landmarks), 1, 1, 50.0, 50.0)
    print_result(len(data) + 1,len(engine.landmarks), mu)