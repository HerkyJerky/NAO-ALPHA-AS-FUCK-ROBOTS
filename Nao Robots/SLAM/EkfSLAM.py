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
    
Jacobian
    
'''
def ekfSlam(data, num_steps, num_landmarks, motion_noise, measurement_noise, initialX, initialY):
    """
    Runs EKF Slam algorithm on given data.
    """
    
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
    dim = 3 + 2*num_landmarks
    mu_0 = numpy.zeros(dim)
    Sigma_0 = numpy.zeros((dim, dim))
    
    for i in range(3, dim):
        Sigma_0[i, i] = float("inf")
        
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
    print "Printing Data Matrix:"
    printMatrix(data)
    print "End printing Data Matrix"
    mu = ekfSlam(data, numSteps, num_landmarks, motion_noise, measurement_noise, 50.0, 50.0)
    print_result(numSteps,num_landmarks, mu)