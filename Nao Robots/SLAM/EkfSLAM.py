'''
Created on 7 nov. 2013

@author: Dennis
'''

from AbstractSLAMProblem import AbstractSLAMProblem;
import math;
import numpy;
import SLAM;

# The square root of the constant below is the minimum distance that needs to separate
# 2 landmarks for the algorithm to treat them as being different landmarks
ASSOCIATE_LANDMARK_THRESHOLD = 0.0001

'''
TODO:

Somehow initialize and allow for configuration of following values:

    self.motion_noise
    self.measurement_noise_range
    self.measurement_noise_bearing
    
I assume these values are all also used by GraphSLAM, so perhaps we should plug these in the common
interface's constructor? And make setters for them to allow configuration through GUI

TODO:

Ensure that in every place where self.P is updated, we also update self.P_top_left

TODO:

Ensure that for every member variable (every var with self.<name> in constructor), there is no variable
with same name without the <self.> stuff in front of it in algorithm
'''

'''
Precompute some values/arrays which are reused often
'''
RANGE_0_3 = range(0, 3)                         # we often need to loop through arrays/matrices with dimension of 3
EYE_2 = numpy.eye(2)                            # 2x2 identity matrix

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

class EkfSLAM(SLAM):
    
    def __init__(self):
        self.num_landmarks_observed = 0
        self.dim = 3
        self.X = numpy.zeros(3)
        self.P = numpy.zeros((3, 3))
        
        self.measurement_data = []
        self.motion_data = []
        
        '''
        Above is stuff which definitely needs to stay in memory.
        
        Below are some matrices which are used so often/remain mostly similar throughout steps,
        that it seems like a good idea to keep them in memory as well instead of re-creating them whenever
        they're needed.
        '''
        
        '''
        A: Jacobian of the prediction model. Initialized as 3x3 Identity matrix
        '''
        self.A = numpy.eye(3)
        
        '''
        Top-left 3x3 corner of P. 
        
        Yes, keeping these values in memory again. Often need to do matrix multiplications specifically 
        with only this part, so it seems more efficient to keep this specific part in memory twice 
        (once as part of the big matrix P, and once separately here) than it is to copy values over from
        the big matrix every time we need them in a separate matrix for matrix multiplication
        '''
        self.P_top_left = numpy.zeros((3, 3))
    
    def reset(self):
        self.num_landmarks_observed = 0
        self.dim = 3
        self.X = numpy.zeros(3)
        self.P = numpy.zeros((3, 3))
        
        self.measurement_data = []
        self.motion_data = []
        
        # no need to reset self.A, since the entries which might have changed since initialization will change every step again anyway.
        
        # still do need to reset self.P_top_left
        self.P_top_left = numpy.zeros((3, 3))
    
    def send_data(self, measurement_data, motion_data):
        self.measurement_data.append(measurement_data)
        self.motion_data.append(motion_data)
    
    def set_parameter(self, parameter_name, value):
        raise NotImplementedError("The set_paramter method of this SLAM algorithm has not yet been implemented!")
    
    def run_slam(self):
        '''
        Runs EKF Slam algorithm on given data.
        
        Expected format of input:
            motion_data is a 2 dimensional array where
            motion_data[i] gives [time,action,dForwards,dSideways,dtheta,speed] at time-step i
            
            measurement_data is a 3 dimensional array where
            measurement_data[i][j] gives [distance(robot, landmark), relative angle] 
            measured at time-step i with respect to the j'th landmark observed at that time-step
        '''
        
        num_steps = len(self.motion_data)
        
        # TODO: debug message, remove this as optimization when everything is confirmed to work correctly
        if(num_steps != len(self.measurement_data)):
            print "Size of measurement data does not equal size of motion data. Probably forgot to send measurement data when no landmarks were observed?"
            print "Should send empty array in that case. Actually, if Graph SLAM also needs this, might be good idea to refactor so we only have a"
            print "send_data method. That way we enforce to always receive equal amount of data stuff"
            print "Since stuff will go horribly wrong if we continue now, I'm returning instead."
            return 
            
        '''
        =============== LOOP THROUGH ALL TIME STEPS ===============
        '''
        for step in range(0, num_steps): 
            motion_data_step = self.motion_data[step]
            measurement_data_step = self.measurement_data[step]
            
            dForwards = motion_data_step[2]
            dSideways = motion_data_step[3]
            dthetaRobot = normalizeAngle(motion_data_step[4])
            
            theta = self.X[2]
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            
            dxRobot = dForwards * cos_theta + dSideways * sin_theta
            dyRobot = dForwards * sin_theta + dSideways * cos_theta
            
            theta = normalizeAngle(theta + dthetaRobot)
            
            self.X[0] = self.X[0] + dxRobot
            self.X[1] = self.X[1] + dyRobot
            self.X[2] = theta
            
            # =============== Step 1: Update current state using the odometry data ===============
            
            # update A according to page 37 of SLAM for dummies
            self.A[0, 2] = - dyRobot
            self.A[1, 2] = dxRobot
            
            # update Q (= a 3x3 matrix used for movement noise) according to page 37 of SLAM for dummies
            c = self.motion_noise
            
            # TODO: if we're really desparate for optimization, or really bored, can precompute some of these multiplications and re-use
            
            Q = [[c*dxRobot*dxRobot,      c*dxRobot*dyRobot,     c*dxRobot*dthetaRobot    ],
                 [c*dyRobot*dxRobot,      c*dyRobot*dyRobot,     c*dyRobot*dthetaRobot    ],
                 [c*dthetaRobot*dxRobot,  c*dthetaRobot*dyRobot, c*dthetaRobot*dthetaRobot]]
            
            # Calculate covariance for robot position
            
            # calculate changes: Pnew = A * P_top_left * A + Q
            self.P_top_left = numpy.add( numpy.dot(numpy.dot(self.A, self.P_top_left), self.A), Q )
            
            # insert entries back into Sigma
            for i in RANGE_0_3:
                for j in RANGE_0_3:
                    self.P[i, j] = self.P_top_left[i, j]
            
            # update robot to feature cross-relations according to page 38 of SLAM for dummies
            # start with top 3 rows of Sigma excluding the first 3 columns
            P_ri = numpy.zeros((3, self.num_landmarks_observed*2))
            
            range_3_dim = range(3, self.dim)
            
            for i in RANGE_0_3:
                for j in range_3_dim:
                    P_ri[i, j - 3] = self.P[i, j]       # fill P_ri with current values in Sigma
                    
            # calculate changes: P_ri = A P_ri
            P_ri = numpy.dot(self.A, P_ri)
            
            # insert entries back into Sigma
            for i in RANGE_0_3:
                for j in range_3_dim:
                    self.P[i, j] = P_ri[i, j - 3]
                    
            # Next, we're gonna look at landmarks. If no landmarks have been observed at all, we can already continue
            # to the next time-step
            if(len(measurement_data_step) == 0):
                continue
                    
            # figure out which landmarks were seen before and which landmarks are new
            reobserved_landmarks = []
            newly_observed_landmarks = []
            
            '''
            save each landmark in one of the 2 arrays above in the following format:
            landmark = [measured_x, measured_y, landmark_index]
            
            The lowest landmark_index possible is 3. A landmark_index will indicate where the 
            first piece of data for that landmark can be found in the X vector. This means
            that there are only uneven landmark indices (since for each landmark, there are 2 pieces
            of data in the X vector)
            '''
            
            for i in xrange(len(measurement_data_step)):
                data_landmark = measurement_data_step[i]        # = [distance(robot, landmark), relative angle] for the specific landmark
                
                distance = data_landmark[0]
                relativeAngle = data_landmark[1]
                angle = normalizeAngle(theta + relativeAngle)
                xDistance = distance * math.cos(angle)
                yDistance = distance * math.sin(angle)
                
                landmark_x = self.X[0] + xDistance
                landmark_y = self.X[1] + yDistance
                
                insertLandmark(landmark_x, landmark_y, self.X, reobserved_landmarks, newly_observed_landmarks, distance, relativeAngle)
                    
            # =============== Step 2: Update state from re-observed landmarks ===============
            for i in xrange(len(reobserved_landmarks)):
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
                landmark = reobserved_landmarks[i]
                landmarkIndex = landmark[2]
                
                dx = self.X[0] - X[landmarkIndex]
                dy = self.X[1] - X[landmarkIndex + 1]
                rSquared = dx*dx + dy*dy
                r = math.sqrt(rSquared)
                
                H_A = dx / r 
                H_B = dy / r 
                H_D = -dy / rSquared
                H_E = dx / rSquared         # SLAM for dummies had a minus in front of this, 2 other sources don't
                
                H = numpy.zeros((2, self.dim))
                H[0, 0] = H_A
                H[0, 1] = H_B
                H[0, 2] = 0.0
                H[0, landmarkIndex    ] = -H_A
                H[0, landmarkIndex + 1] = -H_B
                
                H[1, 0] = H_D
                H[1, 1] = H_E
                H[1, 2] = -1.0
                H[1, landmarkIndex    ] = -H_D
                H[1, landmarkIndex + 1] = -H_E
                
                H_transpose = numpy.transpose(H)    
                
                # R =    rc    0
                #        0    bd
                #
                # where c = measurement noise constant for range, bd = measurement noise for bearing
                R = [[r*self.measurement_noise_range,                              0],
                     [                             0, self.measurement_noise_bearing]]
                
                # Kalman gain K (see description above function definition) = P * H^T * (H * P * H^T + V * R * V^T)^-1
                # V = 2x2 identity matrix
                
                # TODO: check if this can't be made more memory efficient by re-using same variable in intermediate steps
                PH_transpose = numpy.dot(self.P, H_transpose)
                HPH_transpose = numpy.dot(H, PH_transpose)
                VR = numpy.dot(EYE_2, R)
                VRV_transpose = numpy.dot(VR, EYE_2)            # EYE_2_TRANSPOSE = EYE_2
                LargeTermInBrackets = numpy.add(HPH_transpose, VRV_transpose)
                Inverse = numpy.linalg.inv(LargeTermInBrackets)
                
                K = numpy.dot(PH_transpose, Inverse)
                
                # h =    [  range  ] from new            z =    [  range  ] from old
                #        [ bearing ] observation                [ bearing ] observations
                dxNew = self.X[0] - landmark[0]
                dyNew = self.X[1] - landmark[1]
                rNew = math.sqrt(dxNew*dxNew + dyNew*dyNew)
                
                # technically should subtract robot's theta from both values below, but since we only use these
                # variables by subtracting them from each other, those terms will cancel out. OPTIMIZATION FTW!!
                bearingPrevious = normalizeAngle(math.atan2(dy, dx))          # -X[2]
                bearingNew = normalizeAngle(math.atan2(dyNew, dxNew))         # -X[2]
                
                z = [r, bearingPrevious]
                h = [rNew, bearingNew]
                
                # X = X + K * (z - h)
                zMinh = numpy.subtract(z, h)
                print "z - h = [" + str(zMinh[0]) + ", " + str(zMinh[1]) + "]"
                K_zMinh = numpy.dot(K, zMinh)
                self.X = numpy.add(self.X, K_zMinh)
                self.X[2] = normalizeAngle(self.X[2])
                
                # P = (I - K * H) * P
                EYE = numpy.eye(self.dim)
                KH = numpy.dot(K, H)
                self.P = numpy.dot(  numpy.subtract(EYE, KH),    self.P   )
                
                self.P_top_left =   [[self.P[0,0],  self.P[0,1],    self.P[0,2]],
                                     [self.P[1,0],  self.P[1,1],    self.P[1,2]],
                                     [self.P[2,0],  self.P[2,1],    self.P[2,2]]]
                
            # =============== Step 3: Add new landmarks to the current state ===============
            for i in xrange(len(newly_observed_landmarks)):
                landmark = newly_observed_landmarks[i]
                
                self.num_landmarks_observed += 1
                self.dim = 3 + 2*self.num_landmarks_observed
                
                # add landmark x and y to X
                x = landmark[0]
                y = landmark[1]
                self.X = numpy.append(self.X, [x, y])
                
                r = landmark[3]
                bearing = landmark[4]
                
                '''
                Compute covariance for the new landmark and insert it in lower right corner of P
                
                P_N1_N1 = Jxr P Jxr^T + Jz R Jz^T
                
                
                R =    rc    0
                       0    bd
                
                where c = measurement noise constant for range, bd = measurement noise for bearing
                '''
                dx = self.X[0] - x
                dy = self.X[1] - y
                
                R = [[r*self.measurement_noise_range,                              0],
                     [                             0, self.measurement_noise_bearing]]
                
                theta_plus_bearing = theta + bearing
                sin_theta_plus_bearing = math.sin(theta_plus_bearing)
                cos_theta_plus_bearing = math.cos(theta_plus_bearing)
                r_sin = r*sin_theta_plus_bearing
                r_cos = r*cos_theta_plus_bearing
                
                # TODO: can optimize this matrix in the same way as self.A, since 4 out of 6 elements always are the same
                Jxr = [[1, 0, -r_sin],
                       [0, 1, r_cos]]
                
                Jz = [[cos_theta_plus_bearing, -r_sin],
                      [sin_theta_plus_bearing, r_cos]]
                
                Jxr_transpose = numpy.transpose(Jxr)
                Jz_transpose = numpy.transpose(Jz)
                
                # executing matrix multiplications one by one to avoid long line with lots of brackets.
                # re-using the same variables to save memory
                
                P_New = numpy.dot(Jxr, self.P_top_left)             # Jxr * P_top_left
                P_New = numpy.dot(P_New, Jxr_transpose)             # Jxr * P_top_left * Jxr^T
                Temp = numpy.dot(Jz, R)                             # Jz * R
                Temp = numpy.dot(Temp, Jz_transpose)                # Jz * R * Jz^T
                P_New = numpy.add(P_New, Temp)                      # Jxr * P_top_left * Jxr^T + Jz * R * Jz^T
                
                self.P = numpy.append(self.P, numpy.zeros((self.dim - 2, 2)), 1)       # add space for 2 more columns
                self.P = numpy.append(self.P, numpy.zeros((2, self.dim)), 0)           # add space for 2 more rows
                
                # insert values
                self.P[self.dim-2, self.dim-2] = P_New[0, 0]
                self.P[self.dim-2, self.dim-1] = P_New[0, 1]
                self.P[self.dim-1, self.dim-2] = P_New[1, 0]
                self.P[self.dim-1, self.dim-1] = P_New[1, 1]
                
                '''
                Compute robot to landmark covariance and insert in first 3 columns, last 2 rows of P
                
                Re-use P_New variable to save memory
                
                P_New = P_top_left * Jxr^T 
                '''
                P_New = numpy.dot(self.P_top_left, Jxr_transpose)
                
                # insert values
                self.P[0, self.dim - 2] = P_New[0, 0]
                self.P[0, self.dim - 1] = P_New[0, 1]
                self.P[1, self.dim - 2] = P_New[1, 0]
                self.P[1, self.dim - 1] = P_New[1, 1]
                self.P[2, self.dim - 2] = P_New[2, 0]
                self.P[2, self.dim - 1] = P_New[2, 1]
                
                '''
                Transpose robot to landmark covariance in order to get landmark to robot covariance. 
                Insert values in first 3 rows, last 2 columns of P
                
                Re-use P_New variable again to save memory
                '''
                
                # TODO: can probably optimize this transpose function call away by thinking (ouch headache!) about
                # where elements would end up in a transpose, since we're accessing entries manually afterwards anyway
                P_New = numpy.transpose(P_New)
                
                # insert values
                self.P[self.dim - 2, 0] = P_New[0, 0]
                self.P[self.dim - 2, 1] = P_New[0, 1]
                self.P[self.dim - 2, 2] = P_New[0, 2]
                self.P[self.dim - 1, 0] = P_New[1, 0]
                self.P[self.dim - 1, 1] = P_New[1, 1]
                self.P[self.dim - 1, 2] = P_New[1, 0]
                
                '''
                Add landmark to landmark covariance to the last 2 rows:
                
                P_New = Jxr * (P_ri)
                
                P_ri are the first 3 rows of P excluding the first 3 columns (and the newly added last 2 columns). 
                P_ri was already computed in step 1, can re-use the variable here
                '''
                P_New = numpy.dot(Jxr, P_ri)
                
                # insert values
                for col in range(3, self.dim - 3):
                    self.P[self.dim - 2, col] = P_New[0, col - 3]
                    self.P[self.dim - 1, col] = P_New[1, col - 3]
                    
                '''
                Finally, the same values transposed need to be added to the last 2 columns
                '''
                    
                # TODO: same optimization as above, get rid of transpose
                P_New = numpy.transpose(P_New)
                
                # insert values
                for row in range(3, self.dim - 3):
                    self.P[row, self.dim - 2] = P_New[row - 3, 0]
                    self.P[row, self.dim - 1] = P_New[row - 3, 1]
                    
                # In case we see multiple landmarks in this single time-step, need to update P_ri now.
                # TODO: Optimization! Should declare P_ri outside the very first loop through timesteps
                P_ri = numpy.zeros((3, self.num_landmarks_observed*2))
                range_3_dim = range(3, self.dim)
                
                for i in RANGE_0_3:
                    for j in range_3_dim:
                        P_ri[i, j - 3] = self.P[i, j]       # fill P_ri with current values in P
        
        self.measurement_data = []
        self.motion_data = []    
        return self.X 

def insertLandmark(x, y, X, reobserved_landmarks, newly_observed_landmarks, r, bearing):
    '''
    Inserts a landmark observed at position (x, y) in either the array reobsered_landmarks
    if it was observed before, or newly_observed_landmarks if it was not observed before.
    
    Uses current state vector X to compare to previously seen landmarks.
    
    Landmarks will be inserted into the correct array in the following format:
    landmark = [measured_x, measured_y, landmark_index, range, bearing]
    
    The lowest landmark_index possible is 3. A landmark_index will indicate where the 
    first piece of data for that landmark can be found in the X vector. This means
    that there are only uneven landmark indices (since for each landmark, there are 2 pieces
    of data in the X vector)
    '''
    for i in xrange(3, len(X), 2):
        x_other = X[i]
        y_other = X[i + 1]
        
        dx = x - x_other
        dy = y - y_other
        
        if((dx*dx + dy*dy) <= ASSOCIATE_LANDMARK_THRESHOLD):
            reobserved_landmarks.append([x, y, i, r, bearing])
            # print "LANDMARKS ASSOCIATED"
            return
    
    new_index = len(X) + len(newly_observed_landmarks)
    newly_observed_landmarks.append([x, y, new_index, r, bearing])
    
TWO_PI = math.pi*2
    
'''
Returns a given angle theta, normalized to lie in [-pi, pi]
'''
def normalizeAngle(theta):
    theta = theta % TWO_PI
    
    if(theta >= 0):
        if(theta < math.pi):
            return theta
        else:
            return theta - TWO_PI
    elif(theta >= -math.pi):
        return theta
    else:
        return theta + TWO_PI
            
def printArray(args, name = ""):
    print name + ":"
    print(args)
    
def printMatrix(matrix, matrix_name = ""):
    print ""
    print "Matrix " + matrix_name + " = "
    for row in matrix:
        printArray([str(x) for x in row])
        
def printSystemState(time_step, X):
    print ""
    print "X after time-step " + str(time_step)
    for i in xrange(len(X)):
        print str(X[i])
    print ""

'''
This is the test case. I will just assume some numbers to check if it actually works
''' 
if __name__ == "__main__":
    PRINT_ROBOT_LOCATIONS = True
    PRINT_ROBOT_LOCATION_ERRORS = False
    ERROR_THRESHOLD = 0.5
    PRINT_LANDMARK_LOCATIONS = True
    
    num_steps = 50
    num_landmarks = 3
    world_size = 75
    measurement_range = 25
    motion_noise = 0.01
    measurement_noise = 0.01
    distance = 2
    
    problem = AbstractSLAMProblem(world_size, measurement_range, 0.01, 0.01, num_landmarks)
    data = problem.run_simulation_dennis(num_steps, num_landmarks, world_size, measurement_range, 0.01, 0.01, distance)
    
    results = ekfSlam(data[2], data[3], num_steps, motion_noise, measurement_noise, measurement_noise, 0, 0)
    
    true_robot_positions = data[0]
    
    if PRINT_ROBOT_LOCATIONS:
        for step in xrange(num_steps):
            X = results[step]
            robot = true_robot_positions[step]
            
            true_x = robot[0]
            true_y = robot[1]
            true_theta = normalizeAngle(robot[2])
            
            estimate_x = X[0]
            estimate_y = X[1]
            estimate_theta = X[2]
            
            print ""
            print "STEP " + str(step)
            print "True robot x = " + str(true_x) + ", estimated robot x = " + str(estimate_x)
            print "True robot y = " + str(true_y) + ", estimated robot y = " + str(estimate_y)
            print "True robot theta = " + str(true_theta) + ", estimated robot theta = " + str(estimate_theta)
            
            for i in xrange(3, len(X), 2):
                print "Landmark " + str(i - 3) + ": ( " + str(X[i]) + ", " + str(X[i+1]) + ")"
            
            print ""
            
    if PRINT_ROBOT_LOCATION_ERRORS:
        for step in xrange(num_steps):
            X = results[step]
            robot = true_robot_positions[step]
            
            true_x = robot[0]
            true_y = robot[1]
            true_theta = normalizeAngle(robot[2])
            
            estimate_x = X[0]
            estimate_y = X[1]
            estimate_theta = X[2]
            
            error_x = true_x - estimate_x
            error_y = true_y - estimate_y
            error_theta = true_theta - estimate_theta
            
            print ""
            print "STEP " + str(step)
            if(abs(error_x) >= ERROR_THRESHOLD):
                print "ERROR ABOVE THRESHOLD! True robot x = " + str(true_x) + ", estimated robot x = " + str(estimate_x)
            if(abs(error_y) >= ERROR_THRESHOLD):
                print "ERROR ABOVE THRESHOLD! True robot y = " + str(true_y) + ", estimated robot y = " + str(estimate_y)
            if(abs(error_theta) >= ERROR_THRESHOLD):
                print "ERROR ABOVE THRESHOLD! True robot theta = " + str(true_theta) + ", estimated robot theta = " + str(estimate_theta)
            print ""
            
    if PRINT_LANDMARK_LOCATIONS:
        landmarks = data[1]
        for i in xrange(len(landmarks)):
            landmark = landmarks[i]
            print "LANDMARK " + str(i) + " at: (" + str(landmark[0]) + ", " + str(landmark[1]) + ")"
            print ""
        
        X = results[len(results) - 1]
        for i in xrange(3, len(X), 2):
            print "Landmark detected at (" + str(X[i]) + ", " + str(X[i+1]) + ")"