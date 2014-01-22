'''
Created on 7 nov. 2013

@author: Taghi
@author: Dennis
'''
     
from AbstractSLAMProblem import *
from CommonFunctionality import *
import numpy

class GraphSLAM:

    def __init__(self):
        print "Initialized Graph SLAM"
    
    def graphSlam(self,data, N, num_landmarks_seen, motion_noise, measurement_noise, initialX = 0, initialY = 0):
        #dim = 2*(N + num_landmarks)
        
        # Initialize 2x2 zeros matrix to start with. Meaning one motion?
        # Afterwards we have to append stuff to matrix. We can not assume that we will see landmarks all the time
        # Also, idea : We can make use of data for dim
        dim = 2 * (N + num_landmarks_seen)
        
        #Omega = numpy.zeros(2,2)
        Omega = numpy.zeros((dim,dim))
        booleans = numpy.zeros((num_landmarks_seen))
        Omega[0,0] = 1.0
        Omega[1,1] = 1.0
        Xi = numpy.zeros((dim,1))
        Xi[0,0] = initialX
        Xi[1,0] = initialY
        
        # Have you ever seen watchmen asked me Gabi at this point
        
        # This loop is just for motions. Measurements might be easily added to data array and it is good to go bitches
        for k in range(len(data)):
            n = k * 2
            measurements = data[k][0]
            motion = data[k][1][0]
            for i in range(len(measurements)):
                one_measurement = measurements[i]
                # Check if we have actually seen something there and if there is something to read at all.
                # This should fix issue we had before with graph slam.
                if (len(one_measurement)!=0):
                    m = 2 * (N + one_measurement[0])
                    post = one_measurement[3]
                    booleans[one_measurement[0]] = post
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
        
        return [mu,booleans]
    
    def print_result(self,num_steps, num_landmarks, result):
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
                
                
    def slam_experiment(self,num_steps, num_landmarks, world_size, 
                                  measurement_range, motion_noise, measurement_noise, distance, error = 0.25):
        # For now, I am asking for exactly the parameters that run_simulation_dennis method needs + world_size
        simulation = AbstractSLAMProblem(world_size, measurement_range, motion_noise, measurement_noise, num_landmarks)  
        # running the simulation
        simulation.run_simulation_dennis(1, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance) 
        # Reading data after simulation
        gabi_array = simulation.observed_motions
        roel_array = simulation.observed_measurements
        
        # Creating engine for pre-processing and making data array
        engine = CommonFunctionality(error)
        data = engine.make_data(gabi_array,roel_array)
        # Making calculations.
        calculation_motion_noise = 2.0
        calculation_measurement_noise = 2.0
        [mu,booleans] = self.graphSlam(data,len(data) + 1,len(engine.landmarks),calculation_motion_noise,calculation_measurement_noise)
        
        #engine.landmarks = self.post_process_landmarks(engine.landmarks)
        self.print_result(len(data) + 1,len(engine.landmarks),mu)
        
    def post_process_landmarks(self,landmarks):
        # This method will post_process landmarks and return different ones.
        new_landmarks = []
        for i in range(len(landmarks)):
            landmark = landmarks[i]
            index = -1
            for k in range(len(new_landmarks)):
                if (landmark[0] == new_landmarks[k][0] and landmark[1] == new_landmarks[k][1]):
                    index = k
            if (index == -1):
                new_landmarks.append(landmark)
        
        return new_landmarks
        
                   
    '''
    This is the test case. I will just assume some numbers to check if it actually works
    ''' 
    if __name__ == "__main__":
        #numSteps = 3
        world_size = 100.0
        measurement_range = 50.0
        walkingDistancePerStep = 3.0
        num_landmarks = 2
        measurement_noise = 1.0
        motion_noise = 1.0
        
        #problem = AbstractSLAMProblem(world_size, measurement_range, motion_noise, measurement_noise, num_landmarks)
        engine = CommonFunctionality()
        # Moves 2 towards x, 2 towards y, turn 45 degrees and goes 4 towards x in that direction.
        gabi_array = [[0,3,2,0,0,10],[1,3,0,2,0,10],[1,3,3,0,0,10],[1,3,0,0,math.pi/2,10]]
        # Structure of roel array : [d(r,l),relAngle] of landmarks seen at time step t.
        roel_array = [[],[],[],[]]
        #data = problem.run_simulation(numSteps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, walkingDistancePerStep);
        data = engine.make_data(gabi_array, roel_array)
        #numSteps = len(data)
        [mu,booleans] = graphSlam(None,data, len(data) + 1, len(engine.landmarks), 1, 1)
        motion_approximations = numpy.zeros((5,3))
        landmarks_approximations = numpy.zeros((num_landmarks,3))

        for k in range(5):

            motion_approximations[k][0] = mu[2*k]
            motion_approximations[k][1] = mu[2*k+1]
            if (k>0):
                motion_approximations[k][2] = data[k - 1][1][0][2]
            else:
                motion_approximations[k][2] = 0.0
        print 'length',len(engine.landmarks)
        print booleans
        for i in range(len(engine.landmarks)):
            landmarks_approximations[i][0] = mu[2*(4 + i)]
            landmarks_approximations[i][1] = mu[2*(4 + i) + 1]
            landmarks_approximations[i][2] = booleans[i]

        #print landmarks_approximations
        #print motion_approximations
        result = numpy.array([motion_approximations,landmarks_approximations])
        print_result(None,len(data) + 1,len(engine.landmarks), mu)
        
        
        