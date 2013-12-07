'''
Created on 2 Dec 2013

@author: Taghi
'''

import math

class CommonFunctionality:
    
    def __init__(self):
        self.landmarks = []
    
    def make_data(self,motion_array,measurement_array,initialX = 0,initialY = 0):
        '''
        This method is same as run_simulation but points are not random. I get data from Roel and others and put it in data
        array which is used by graph slam algo. Structure of array is same as before. But I will try to think of some way
        to deal with non square array thing. Idea is that, size of data array is size of motion array but we also append
        landmarks to it. So, if we haven`t seen anything at that moment, we won`t update our matrix with any data about landmarks
        but motion will still be updated. So, to summarize, every element of data is one whole step of motion and measurements.
        As already mentioned at time step t, motion at t is data[t][1] and measurements of time step t is data[t][0]
        '''
        
        pre_processed = self.pre_process_data(motion_array,measurement_array,initialX,initialY)
        
        processed_motion_array = pre_processed[0]
        processed_measurement_array = pre_processed[1]
        
        data = []
            
        # We do not need any randomness, so we will just go through arrays and add data
            
        numSteps = len(processed_motion_array)
            
        # This part should be clarified, because I am not sure how data is going to be send around
        # My assumption : measurement_array has measurement send from Roel but we update that array with newer one before sending it here where indices are specified as well
        # For motion I assume it is an array that has dx and dy in it. Some preprocessing might be needed
        # Preprocessing needed might be about addind data send by Gabi to history of motions in case Gabi sends only last motion.
            
        # For now this method just loops through two arrays and appends them in a way that was done before.
        # This might need some altering.
            
        for k in range(numSteps):
                
            data.append([processed_measurement_array[k],processed_motion_array[k]])
                
        return data
    
    
    def pre_process_data(self,gabi_array,roel_array,initialX,initialY):
        
        '''
        Method that pre processes data to make it usable for make_data method.
        Information we get from gabi : [time,action,dx,dy,dtheta,speed]
        Information we get from roel : [d(r,l),relativeAngle]
        '''
        gabi_data = []
        roel_data = []
        orientation = 0;
        '''
        Processing of gabi`s informations.
        I read actions,dx,dy and dtheta at each step. I update orientation of robot
        and then I add new data to gabi_data array, adding last movement and I guess size of Gabi and Roel`s arrays are same
        '''
        for i in range(len(gabi_array)):
            motion_info = gabi_array[i]
            action = motion_info[1]
            dx = motion_info[2]
            dy = motion_info[3]
            dtheta = motion_info[4]
            orientation += dtheta
            gabi_data.append([dx * math.cos(orientation),dy * math.sin(orientation)])
            #Keeping rough estimate of where we are for each step
            
            initialX += dx*math.cos(orientation)
            initialY += dy*math.sin(orientation)
            
            #Processing Roel`s data which is of format [d(r,l),relAngle]
            
            # Accessing data from time step i.
            # It might have more than one sensed landmark, so we will loop through for each of them
            
            sense_data = roel_array[i]
            for k in range(len(sense_data)):
                distanceToLand = sense_data[k][0]
                relativeAngle = sense_data[k][1]
                xDistance = distanceToLand * math.cos(relativeAngle)
                yDistance = distanceToLand * math.sin(relativeAngle)
                roughXlandmark = initialX + xDistance
                roughYlandmark = initialY + yDistance
                index = self.landmark_check(roughXlandmark,roughYlandmark)
                roel_data.append([index,xDistance,yDistance])
            
        
        return [gabi_data,roel_data]
    
    def landmark_check(self,roughNewLandmarkX,roughNewLandmarkY):
        
        threshold = 1 #Threshold value for euclidean distance between two landmarks
        threshold = threshold*threshold
        
        indexFound = -1
        
        for k in range(len(self.landmarks)):
            landmark = self.landmarks[k]
            xDistance = math.pow(roughNewLandmarkX - landmark[0], 2)
            yDistance = math.pow(roughNewLandmarkY - landmark[1], 2)
            if ((xDistance + yDistance) < threshold):
                # This means landmark is way too similar, so should just give it an existing index.
                indexFound = k
        
        if (indexFound == -1):
            # Means we  did not find this landmark
            self.landmarks.append([roughNewLandmarkX,roughNewLandmarkY])
            indexFound = len(self.landmarks) - 1
                
        return [indexFound]     