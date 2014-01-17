'''
Created on 2 Dec 2013

@author: Taghi
'''

import math

class CommonFunctionality:
    
    def __init__(self,error = 0.25):
        self.landmarks = []
        self.threshold_landmark_error = error
    
    def make_data(self,motion_array,measurement_array,initialX = 0,initialY = 0):
        '''
        This method is same as run_simulation but points are not random. I get data from Roel and others and put it in data
        array which is used by graph slam algo. Structure of array is same as before. But I will try to think of some way
        to deal with non square array thing. Idea is that, size of data array is size of motion array but we also append
        landmarks to it. So, if we haven`t seen anything at that moment, we won`t update our matrix with any data about landmarks
        but motion will still be updated. So, to summarize, every element of data is one whole step of motion and measurements.
        As already mentioned at time step t, motion at t is data[t][1] and measurements of time step t is data[t][0]
        '''
        data = []
        
        # Changed method so that it returns whole data array for once(without separations, it just puts all together)
        data = self.pre_process_data(motion_array,measurement_array,initialX,initialY)
        
            
        # We do not need any randomness, so we will just go through arrays and add data
          
        # This part should be clarified, because I am not sure how data is going to be send around
        # My assumption : measurement_array has measurement send from Roel but we update that array with newer one before sending it here where indices are specified as well
        # For motion I assume it is an array that has dx and dy in it. Some preprocessing might be needed
        # Preprocessing needed might be about addind data send by Gabi to history of motions in case Gabi sends only last motion.
  
                
        return data
    
    
    def pre_process_data(self,gabi_array,roel_array,initialX,initialY):
        
        '''
        Method that pre processes data to make it usable for make_data method.
        Information we get from gabi : [time,action,dx,dy,dtheta,speed]
        Information we get from roel : [d(r,l),relativeAngle]
        '''
        result = []
        orientation = 0;
        '''
        Processing of gabi`s informations.
        I read actions,dx,dy and dtheta at each step. I update orientation of robot
        and then I add new data to gabi_data array, adding last movement and I guess size of Gabi and Roel`s arrays are same
        '''
        for i in range(len(gabi_array)):
            gabi_data = []
            roel_data = []
            motion_info = gabi_array[i]
            #Only adding data from gabi if it is of type 3(move/rotate)
            forwardMove = motion_info[2]
            sideMove = motion_info[3]
            dtheta = motion_info[4]
            orientation += dtheta
            dx = forwardMove * math.cos(orientation) + sideMove * math.sin(orientation)
            dy = forwardMove * math.sin(orientation) + sideMove * math.cos(orientation)
            # If orientation is zero, then y might not change.
            # This part is interesting. It basically says that, if there is no orientation, then y can not change?
            # That just sounds silly to me. I guess it moves sideways, soo this code WILL/SHOULD CHANGE!!!
            # Ok, changed it. Also, I think we should keep them as being dx and dy as cos and sin are already taken
            # into account.
            gabi_data.append([dx ,dy,orientation])
            #Keeping rough estimate of where we are for each step
            
            initialX += dx
            initialY += dy
            
            #Processing Roel`s data which is of format [d(r,l),relAngle]
            
            # Accessing data from time step i.
            # It might have more than one sensed landmark, so we will loop through for each of them
            
            sense_data = roel_array[i]
            for k in range(len(sense_data)):
                one_sense = sense_data[k]
                if (len(one_sense) != 0):
                    distanceToLand = sense_data[k][0]
                    relativeAngle = sense_data[k][1]
                    post = sense_data[k][2]
                    # Added orientation to relative angle as I think it should be like this
                    # (As discussed with Dennis)
                    xDistance = distanceToLand * math.cos(relativeAngle + orientation)
                    yDistance = distanceToLand * math.sin(relativeAngle + orientation)
                    # Rough estimates of where landmark is (very rough)
                    roughXlandmark = initialX + xDistance
                    roughYlandmark = initialY + yDistance
                    index = self.landmark_check(roughXlandmark,roughYlandmark,post)
                    roel_data.append([index,xDistance,yDistance,post])
            result.append([roel_data,gabi_data])
            
        
        return result
    
    def landmark_check(self,roughNewLandmarkX,roughNewLandmarkY,post):
        
        indexFound = -1
        
        for k in range(len(self.landmarks)):
            landmark = self.landmarks[k]
            if (landmark[2] == post):
                xDistance = math.pow(roughNewLandmarkX - landmark[0], 2)
                yDistance = math.pow(roughNewLandmarkY - landmark[1], 2)
                if ((xDistance + yDistance) <= self.threshold_landmark_error):
                    # This means landmark is way too similar, so should just give it an existing index.
                    indexFound = k
        
        if (indexFound == -1):
            # Means we  did not find this landmark
            self.landmarks.append([roughNewLandmarkX,roughNewLandmarkY,post])
            indexFound = len(self.landmarks) - 1
                
        return indexFound     
    
    
if __name__ == "__main__":
    # This is the test case to see if data will be created correctly
    
    # Structure of gabi array : [time,action,dx,dy,dtheta,speed]
    gabi_array = [[0,3,2,0,0,10],[1,3,0,2,0,10],[2,3,0,0,45,10],[3,3,4,0,0,10]] # Moves 2 towards x, 2 towards y, turn 45 degrees and goes 4 towards x in that direction.
    # Structure of roel array : [d(r,l),relAngle] of landmarks seen at time step t.
    roel_array = [[[5,0,True],[3,0,False]],[[3,0,False],[1,0,False]],[[4,0,False]],[[]]]
    engine = CommonFunctionality()
    data = engine.make_data(gabi_array, roel_array)
    for k in range(len(data)):
        print "Roel:"
        print data[k][0]
        print "Gabi:"
        print data[k][1]
    
