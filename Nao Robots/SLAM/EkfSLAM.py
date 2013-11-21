'''
Created on 7 nov. 2013

@author: Dennis
'''

from AbstractSLAMProblem import AbstractSLAMProblem;
import numpy;

'''
Notes from: 
http://ais.informatik.uni-freiburg.de/teaching/ws12/mapping/pdf/slam04-ekf-slam.pdf  and
http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-412j-cognitive-robotics-spring-2005/projects/1aslam_blas_repo.pdf


==== Definition SLAM Problem ====
Given:
    u_1:T = [u_1, u_2, u_3, ..., u_T] = Robot's controls
    z_1:T = [z_1, z_2, z_3, ..., z_T] = Observations
    
Wanted:
    m = map
    x_0:T = [x_1, x_2, x_3, ..., x_T] = Robot's path
    
State Space:
    x_t = ( x, y, theta,    m_1x, m_1y, ..., m_nx, m_ny )^T    <-- transpose
                |                |                |
            robot's pose    landmark 1        landmark n
            
State Representation for map with n landmarks: (3 + 2n)-dimensional Gaussian

    (   x   )    (      x   x      x   y        x   theta      |      x   m_1,x      x   m_1,y    . . .        x   m_n,x      x   m_n,y    )
    (   y   )    (      y   x      y   y        y   theta      |      y   m_1,x      y   m_1,y    . . .            m_n,x          m_n,y    )
    ( theta )    (    theta x    theta y      theta theta      |    theta m_1,x    theta m_1,y    . . .      theta m_n,x    theta m_n,y    )

    ( m_1,x )    (    m_1,x x    m_1,x y            theta      |    m_1,x m_1,x    m_1,x m_1,y    . . .      m_1,x m_n,x    m_1,x m_n,y    )
    ( m_1,y )    (    m_1,y x    m_1,y y            theta      |    m_1,y m_1,x    m_1,y m_1,y    . . .      m_1,y m_n,x    m_1,y m_n,y    )
    (   .   )    (       .          .              .           |         .              .          .              .              .         )
    (   .   )    (       .          .              .           |         .              .           .             .              .         )
    (   .   )    (       .          .              .           |         .              .            .            .              .         )
    ( m_n,x )    (    m_n,x x    m_n,x y            theta      |    m_n,x m_1,x    m_n,x m_1,y    . . .      m_n,x m_n,x    m_n,x m_n,y    )
    ( m_n,y )    (    m_n,y x    m_n,y y            theta      |    m_n,y m_1,x    m_n,y m_1,y    . . .      m_n,y m_n,x    m_n,y m_n,y    )

        mu = System State                                              Sigma = Covariance Matrix
    
    More compactly:
    
    mu =    (    x    )        Sigma =    (    Sigma_xx    Sigma_xm    )
            (    m    )                   (    Sigma_mx    Sigma_mm    )
            
    Sigma_xx contains covariance on robot position
    
    If Sigma_mx =    D        then D contains covariance between robot state and first landmark,
                    ...
                    ...
                     H        and H contains covariance between robot state and nth landmark.
                     
    If Sigma_xm =    E ... ... I    then E contains covariance between first landmark and robot state,
                                    and I contains covariance between nth landmark and robot state.
                                    
    If Sigma_mm =    B   ...   G    then B contains covariance on first landmark,
                     ... ... ...    G contains covariance between the first landmark and the last landmark
                     ... ... ...    F contains covariance between the last landmark and the first landmark
                     F   ...   C    and C contains covariance on nth landmark

Innovation = difference in estimated robot position from odometry and robot position based on vision.
                  
Kalman gain K =     x_r      x_b
                    y_r      y_b
                    t_r      t_b
                    x_1,r    x_1,b
                    y_1,r    y_1,b
                    . . .    . . .
                    . . .    . . .
                    x_n,r    x_n,b
                    y_n,r    y_n,b

    For every row, the first column shows how much should be gained from the innovation for the corresponding
    row of the system state mu in terms of range, and the second column in terms of bearing (angle).
    
q = movement error term (on command to move 1 unit, robot will move q extra or less)
    
'''
def ekfSlam(data, num_steps, num_landmarks, motion_noise, measurement_noise, initialX, initialY):
    """
    Runs EKF Slam algorithm on given data.
    """
    
    """
    Precompute some values/arrays which are reused often
    """
    RANGE_0_3 = range(0, 3)          # we often need to loop through arrays/matrices with dimension of 3
    
    """ 
    =============== INITIALIZATION =============== 
    mu_0 = ( 0 0 0 ... 0 )^T
    
                    ( 0  0  0    0    . . .    0  )
                    ( 0  0  0    0    . . .    0  )
                    ( 0  0  0    0    . . .    0  )
    Sigma_0 =       ( 0  0  0   inf   . . .    0  )
                    ( .  .  .    .     .       .  )
                    ( .  .  .    .      .      .  )
                    ( .  .  .    .       .     .  )
                    ( 0  0  0    0    . . .   inf )
    """
    num_landmarks_observed = 0
    landmark_observe_counts = numpy.zeros(num_landmarks)
    
    dim = 3 + 2*num_landmarks_observed
    mu = numpy.zeros(dim)
    Sigma = numpy.zeros((dim, dim))
    
    for i in range(3, dim):
        Sigma[i, i] = float("inf")
        
    """
    A: Jacobian of the prediction model. Initialized as 3x3 Identity matrix
    """
    A = numpy.eye(3)
        
    """
    =============== LOOP THROUGH ALL TIME STEPS ===============
    """
    for step in range(0, num_steps): 
        # =============== Step 1: Update current state using the odometry data ===============
        iterationData = data.getIterationData(step)        # THIS FUNCTION DOESNT EXIST YET. Assumed to fetch data of the i'th timestep only
        
        dx = iterationData.dx
        dy = iterationData.dy
        dtheta = iterationData.dtheta
        dx = 2
        dy = 3
        dtheta = 5
        
        mu[0] = mu[0] + dx
        mu[1] = mu[1] + dy
        mu[2] = mu[2] + dtheta
        
        # update A according to page 37 of SLAM for dummies
        # TODO: CHECK! Maybe it should be old values -dy +dx instead of replacing by -dy and +dx ???
        A[0, 2] = - dy
        A[1, 2] = dx
        
        # update Q (= a 3x3 matrix used for movement noise) according to page 37 of SLAM for dummies
        c = motion_noise
        
        Q = [[c*dx*dx,      c*dx*dy,     c*dx*dtheta    ],
             [c*dy*dx,      c*dy*dy,     c*dy*dtheta    ],
             [c*dtheta*dx,  c*dtheta*dy, c*dtheta*dtheta]]
        
        # Calculate covariance for robot position
        # start with top left 3x3 matrix of Sigma
        P = [[Sigma[0,0], Sigma[0,1], Sigma[0,2]],
             [Sigma[1,0], Sigma[1,1], Sigma[1,2]],
             [Sigma[2,0], Sigma[2,1], Sigma[2,2]]]
        
        # calculate changes: Pnew = A P A + Q
        P = numpy.add( numpy.dot(numpy.dot(A, P), A) )
        
        # insert entries back into Sigma
        for i in RANGE_0_3:
            for j in RANGE_0_3:
                Sigma[i, j] = P[i, j]
        
        # update robot to feature cross-relations according to page 38 of SLAM for dummies
        # start with top 3 rows of Sigma excluding the first 3 columns
        P = numpy.zeros(3, num_landmarks)       # we can reuse the P variable since we're done using the data above. Re-initialize it to zeros
        
        range_3_dim = range(3, dim)
        
        for i in RANGE_0_3:
            for j in range_3_dim:
                P[i, j - 3] = Sigma[i, j]       # fill P with current values in Sigma
                
        # calculate changes: Pnew = A P
        P = numpy.dot(A, P)
        
        # insert entries back into Sigma
        for i in RANGE_0_3:
            for j in range_3_dim:
                Sigma[i, j] = P[i, j - 3]
                
        # =============== Step 2: Update state from re-observed landmarks ===============
        for i in iterationData.getObservedLandmarks():
            
        
        # lastly, update dim to accomodate for newly introduced landmarks
        dim = 3 + 2*num_landmarks_observed
        
    return
    
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
            
def printArray(args):
    print "\t".join(args)
    
def printMatrix(matrix):
    for row in matrix:
        printArray([str(x) for x in row])

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
    mu = ekfSlam(data, numSteps, num_landmarks, motion_noise, measurement_noise, 50.0, 50.0)
    print_result(numSteps,num_landmarks, mu)