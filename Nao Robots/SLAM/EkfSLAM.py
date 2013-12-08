'''
Created on 7 nov. 2013

@author: Dennis
'''

from AbstractSLAMProblem import AbstractSLAMProblem;
import math;
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

        X = System State                                              P = Covariance Matrix
    
    More compactly:
    
     X =    (    x    )            P =    (    P_xx    P_xm    )
            (    m    )                   (    P_mx    P_mm    )
            
    P_xx contains covariance on robot position
    
    If P_mx =        D        then D contains covariance between robot state and first landmark,
                    ...
                    ...
                     H        and H contains covariance between robot state and nth landmark.
                     
    If P_xm =        E ... ... I    then E contains covariance between first landmark and robot state,
                                    and I contains covariance between nth landmark and robot state.
                                    
    If P_mm =        B   ...   G    then B contains covariance on first landmark,
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
def ekfSlam(motion_data, measurement_data, num_steps, motion_noise, measurement_noise_range, measurement_noise_bearing, initialX, initialY):
    '''
    Runs EKF Slam algorithm on given data.
    
    Expected format of input:
        motion_data is a 2 dimensional array where
        motion_data[i] gives [time,action,dx,dy,dtheta,speed] at time-step i
        
        measurement_data is a 3 dimensional array where
        measurement_data[i][j] gives [distance(robot, landmark), relative angle] 
        measured at time-step i with respect to the j'th landmark observed at that time-step
    '''
    
    # TODO!!!!!!!!!!!!!!!!!!!!
    # MAKE SURE THAT ANGLES ARE IN CORRECT UNIT FOR SIN() / COS() FUNCTION CALLS
    
    '''
    Precompute some values/arrays which are reused often
    '''
    RANGE_0_3 = range(0, 3)                         # we often need to loop through arrays/matrices with dimension of 3
    EYE_2 = numpy.eye(2)                            # 2x2 identity matrix
    
    ''' 
    =============== INITIALIZATION =============== 
    X_0 = ( 0 0 0 ... 0 )^T
    
                    ( 0  0  0    0    . . .    0  )
                    ( 0  0  0    0    . . .    0  )
                    ( 0  0  0    0    . . .    0  )
    P_0 =           ( 0  0  0   inf   . . .    0  )
                    ( .  .  .    .     .       .  )
                    ( .  .  .    .      .      .  )
                    ( .  .  .    .       .     .  )
                    ( 0  0  0    0    . . .   inf )
    '''
    num_landmarks_observed = 0
    landmark_observe_counts = []
    
    dim = 3 + 2*num_landmarks_observed
    X = numpy.zeros(dim)
    P = numpy.zeros((dim, dim))
    
    for i in range(3, dim):
        P[i, i] = float("inf")
        
    '''
    A: Jacobian of the prediction model. Initialized as 3x3 Identity matrix
    '''
        
    A = numpy.eye(3)
        
    '''
    =============== LOOP THROUGH ALL TIME STEPS ===============
    '''
    for step in range(0, num_steps): 
        motion_data_step = motion_data[step]
        measurement_data_step = measurement_data[step]
        
        dthetaRobot = motion_data_step[4]
        dxRobot = motion_data_step[2] * math.cos(X[2])
        dyRobot = motion_data_step[3] * math.sin(X[2])
        
        X[0] = X[0] + dxRobot
        X[1] = X[1] + dyRobot
        X[2] = X[2] + dthetaRobot
        
        distanceTravelled = math.sqrt(dxRobot*dxRobot + dyRobot*dyRobot)
        
        '''
        Jxr = Jacobian of prediction of landmarks without prediction of theta, with respect to robot state =
            
            1    0    -dyRobot
            0    1     dxRobot
                
        Jz = Jacobian of prediction model for landmarks with respect to range and bearing =
            
            cos(theta + dthetaRobot)    -distanceTravelled * sin(theta + dthetaRobot)
            sin(theta + dthetaRobot)     distanceTravelled * cos(theta + dthetaRobot)
            
        Pre-computing these matrices since we'll be re-using them in a for-loop in step 3
        '''
        Jxr = [[1, 0, -dyRobot],
               [0, 1, dxRobot]]
            
        thetaNew = X[2] + dthetaRobot
        cosTheta = math.cos(thetaNew)
        sinTheta = math.sin(thetaNew)
            
        Jz = [[cosTheta, -distanceTravelled*sinTheta],
              [sinTheta, distanceTravelled*cosTheta]]
        
        Jxr_transpose = numpy.transpose(Jxr)
        Jz_transpose = numpy.transpose(Jz)
        
        # =============== Step 1: Update current state using the odometry data ===============
        
        # update A according to page 37 of SLAM for dummies
        # TODO: CHECK! Maybe it should be old values -dy +dx instead of replacing by -dy and +dx ???
        A[0, 2] = - dyRobot
        A[1, 2] = dxRobot
        
        # update Q (= a 3x3 matrix used for movement noise) according to page 37 of SLAM for dummies
        c = motion_noise
        
        Q = [[c*dxRobot*dxRobot,      c*dxRobot*dyRobot,     c*dxRobot*dthetaRobot    ],
             [c*dyRobot*dxRobot,      c*dyRobot*dyRobot,     c*dyRobot*dthetaRobot    ],
             [c*dthetaRobot*dxRobot,  c*dthetaRobot*dyRobot, c*dthetaRobot*dthetaRobot]]
        
        # Calculate covariance for robot position
        # start with top left 3x3 matrix of P
        P_rr = [[P[0,0], P[0,1], P[0,2]],
                [P[1,0], P[1,1], P[1,2]],
                [P[2,0], P[2,1], P[2,2]]]
        
        # calculate changes: Pnew = A PP A + Q
        P_rr = numpy.add( numpy.dot(numpy.dot(A, P_rr), A), Q )
        
        # insert entries back into Sigma
        for i in RANGE_0_3:
            for j in RANGE_0_3:
                P[i, j] = P_rr[i, j]
        
        # update robot to feature cross-relations according to page 38 of SLAM for dummies
        # start with top 3 rows of Sigma excluding the first 3 columns
        P_ri = numpy.zeros(3, num_landmarks_observed)
        
        range_3_dim = range(3, dim)
        
        for i in RANGE_0_3:
            for j in range_3_dim:
                P_ri[i, j - 3] = P[i, j]       # fill P_ri with current values in Sigma
                
        # calculate changes: P_ri = A P_ri
        P_ri = numpy.dot(A, P_ri)
        
        # insert entries back into Sigma
        for i in RANGE_0_3:
            for j in range_3_dim:
                P[i, j] = P_ri[i, j - 3]
                
        # figure out which landmarks were seen before and which landmarks are new
        reobserved_landmarks = []
        newly_observed_landmarks = []
        
        for i in range(len(measurement_data_step)):
            
                
        # =============== Step 2: Update state from re-observed landmarks ===============
        for i in iterationData.getReObservedLandmarks():
            '''
            H = Jacobian of measurement model =
            
            A    B    C    0    0    -A    -B    0    0
            D    E    F    0    0    -D    -E    0    0
            
            where the negative values are in the 2 columns corresponding to the re-observed landmarks and:
            r = range = distance between robot and landmark
            A = (x_robot - x_landmark) / r
            B = (y_robot - y_landmark) / r
            C = 0
            D = (y_landmark - y_robot) / r^2
            E = (x_landmark - x_robot) / r^2
            F = -1
            
            Note that x_landmark and y_landmark here refer to the currently saved coordinates in the X vector, NOT the new observations
            '''
            landmarkIndex = i.index
            
            dx = X[0] - X[landmarkIndex + 3]
            dy = X[1] - X[landmarkIndex + 4]
            rSquared = dx*dx + dy*dy
            r = math.sqrt(rSquared)
            
            H_A = dx / r 
            H_B = dy / r 
            H_D = -dy / rSquared
            H_E = -dx / rSquared
            
            H = numpy.zeros((2, dim))
            H[0, 0] = H_A
            H[0, 1] = H_B
            H[0, 2] = 0.0
            H[0, landmarkIndex + 3] = -H_A
            H[0, landmarkIndex + 4] = -H_B
            
            H[1, 0] = H_D
            H[1, 1] = H_E
            H[1, 2] = -1.0
            H[1, landmarkIndex + 3] = -H_D
            H[1, landmarkIndex + 4] = -H_E
            
            H_transpose = numpy.transpose(H)    
            
            # R =    rc    0
            #        0    bd
            #
            # where c = measurement noise constant for range, bd = measurement noise for bearing
            R = [[r*measurement_noise_range,                         0],
                 [                        0, measurement_noise_bearing]]
            
            # Kalman gain K (see description above function definition) = P * H^T * (H * P * H^T + V * R * V^T)^-1
            # V = 2x2 identity matrix
            
            PH_transpose = numpy.dot(P, H_transpose)
            HPH_transpose = numpy.dot(H, PH_transpose)
            VR = numpy.dot(EYE_2, R)
            VRV_transpose = numpy.dot(VR, EYE_2)            # EYE_2_TRANSPOSE = EYE_2
            LargeTermInBrackets = numpy.add(HPH_transpose, VRV_transpose)
            Inverse = numpy.linalg.inv(LargeTermInBrackets)
            
            K = numpy.dot(PH_transpose, Inverse)
            
            # h =    [  range  ] from new            z =    [  range  ] from old
            #        [ bearing ] observation                [ bearing ] observations
            dxNew = X[0] - i.x
            dyNew = X[1] - i.y
            rNew = math.sqrt(dxNew*dxNew + dyNew*dyNew)
            
            # technically should subtract robot's theta from both values below, but since we only use these
            # variables by subtracting them from each other, those terms will cancel out. OPTIMIZATION FTW!!
            bearingPrevious = math.atan2(dy, dx)        # -X[3]
            bearingNew = math.atan2(dyNew, dxNew)       # -X[3]
            
            z = [r, bearingPrevious]
            h = [rNew, bearingNew]
            
            # X = X + K * (z - h)
            zMinh = numpy.subtract(z, h)
            K_zMinh = numpy.dot(K, zMinh)
            X = numpy.add(X, K_zMinh)
            
            # finally, increment observation count
            landmark_observe_counts[landmarkIndex] = landmark_observe_counts[landmarkIndex] + 1
            
        # =============== Step 3: Add new landmarks to the current state ===============
        for i in iterationData.getNewlyObservedLandmarks():
            num_landmarks_observed += 1
            dim = 3 + 2*num_landmarks_observed
            
            # add landmark x and y to X
            x = i.x
            y = i.y
            X = numpy.append(X, [x, y])
            
            P = numpy.append(P, numpy.zeros((dim - 2, 2)), 1)       # add space for 2 more columns
            P = numpy.append(P, numpy.zeros((2, dim)), 0)           # add space for 2 more rows
            
            '''
            Compute covariance for the new landmark and insert it in lower right corner of P
            
            P_N1_N1 = Jxr P Jxr^T + Jz R Jz^T
            
            
            R =    rc    0
                   0    bd
            
            where c = measurement noise constant for range, bd = measurement noise for bearing
            '''
            dx = X[0] - x
            dy = X[1] - y
            r = math.sqrt(dx*dx + dy*dy)
            
            R = [[r*measurement_noise_range,                         0],
                 [                        0, measurement_noise_bearing]]
            
            # executing matrix multiplications one by one to avoid long line with lots of brackets.
            # re-using the same variables to save memory
            P_New = numpy.dot(Jxr, P)                           # Jxr * P
            P_New = numpy.dot(P_New, Jxr_transpose)             # Jxr * P * Jxr^T
            Temp = numpy.dot(Jz, R)                             # Jz * R
            Temp = numpy.dot(Temp, Jz_transpose)                # Jz * R * Jz^T
            P_New = numpy.add(P_New, Temp)                      # Jxr * P * Jxr^T + Jz * R * Jz^T
            
            # insert values
            P[dim-1, dim-1] = P_New[0, 0]
            P[dim-1, dim]   = P_New[0, 1]
            P[dim, dim-1]   = P_New[1, 0]
            P[dim, dim]     = P_New[1, 1]
            
            '''
            Compute robot to landmark covariance and insert in first 3 columns, last 2 rows of P
            
            Re-use P_New variable to save memory
            
            P_New = P_rr * Jxr^T where P_rr = top left 3x3 matrix of P
            
            P_rr was computed in step 1 already, so we can re-use that variable here and don't need to initialize it again
            '''
            P_New = P_rr * Jxr_transpose
            
            # insert values
            P[0, dim - 1] = P_New[0, 0]
            P[0, dim    ] = P_New[0, 1]
            P[1, dim - 1] = P_New[1, 0]
            P[1, dim    ] = P_New[1, 1]
            P[2, dim - 1] = P_New[2, 0]
            P[2, dim    ] = P_New[2, 1]
            
            '''
            Transpose robot to landmark covariance in order to get landmark to robot covariance. 
            Insert values in first 3 rows, last 2 columns of P
            
            Re-use P_New variable again to save memory
            '''
            P_New = numpy.transpose(P_New)
            
            # insert values
            P[dim - 1, 0] = P_New[0, 0]
            P[dim - 1, 1] = P_New[0, 1]
            P[dim - 1, 2] = P_New[0, 2]
            P[    dim, 0] = P_New[1, 0]
            P[    dim, 1] = P_New[1, 1]
            P[    dim, 2] = P_New[1, 0]
            
            '''
            Add landmark to landmark covariance to the last 2 rows:
            
            P_New = Jxr * (P_ri)^T
            
            P_ri are the first 3 rows of P excluding the first 3 columns (and the newly added last 2 columns). 
            P_ri was already computed in step 1, can re-use the variable here
            '''
            P_New = numpy.dot(Jxr, numpy.transpose(P_ri))
            
            # insert values
            for col in range(3, dim - 2):
                P[dim - 1, col] = P_New[0, col - 3]
                P[    dim, col] = P_New[1, col - 3]
                
            '''
            Finally, the same values transposed need to be added to the last 2 columns
            '''
            P_New = numpy.transpose(P_New)
            
            # insert values
            for row in range(3, dim - 2):
                P[row, dim - 1] = P_New[row, 0]
                P[row,     dim] = P_New[row, 1]
        
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