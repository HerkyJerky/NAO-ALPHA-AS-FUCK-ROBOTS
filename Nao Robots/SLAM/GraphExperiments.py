'''
Created on 11 Dec 2013

This class contains test cases for Graph SLAM algorithm.

@author: Taghi
'''

from GraphSLAM import *

def test_1():
    num_steps = 100
    num_landmarks = 0
    world_size = 75
    measurement_range = 50
    motion_noise = 0.000001
    measurement_noise = 0.00001
    distance = 2 
    slam = GraphSLAM()
    slam.slam_experiment(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)

def test_2():
    num_steps = 100
    num_landmarks = 0
    world_size = 75
    measurement_range = 50
    motion_noise = 0.1
    measurement_noise = 0.1
    distance = 2
    slam = GraphSLAM()
    slam.slam_experiment(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)

# Might be a better idea to increase error (like to 20)
def test_3():
    ASSOCIATE_LANDMARK_THRESHOLD = 0.0
    num_steps = 100
    num_landmarks = 6
    world_size = 75
    measurement_range = 50
    motion_noise = 0.000001
    measurement_noise = 0.00001
    distance = 2
    slam = GraphSLAM()
    slam.slam_experiment(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance,ASSOCIATE_LANDMARK_THRESHOLD)
    
def test_4():
    ASSOCIATE_LANDMARK_THRESHOLD = 0.001
    num_steps = 100
    num_landmarks = 6
    world_size = 75
    measurement_range = 50
    motion_noise = 0.000001
    measurement_noise = 0.00001
    distance = 2
    slam = GraphSLAM()
    slam.slam_experiment(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance,ASSOCIATE_LANDMARK_THRESHOLD)

def test_5():
    ASSOCIATE_LANDMARK_THRESHOLD = 0.1
    num_steps = 100
    num_landmarks = 6
    world_size = 75
    measurement_range = 50
    motion_noise = 0.000001
    measurement_noise = 0.00001
    distance = 2
    slam = GraphSLAM()
    slam.slam_experiment(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance, ASSOCIATE_LANDMARK_THRESHOLD)

def test_6():
    ASSOCIATE_LANDMARK_THRESHOLD = 1.0
    num_steps = 100
    num_landmarks = 6
    world_size = 75
    measurement_range = 50
    motion_noise = 0.000001
    measurement_noise = 0.00001
    distance = 2
    slam = GraphSLAM()
    slam.slam_experiment(num_steps, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance, ASSOCIATE_LANDMARK_THRESHOLD)


if __name__ == "__main__":
    # Here we will call one of the test cases. Just comment out whichever you want to run.
    #test_1()
    #test_2()
    test_3()
    #test_4()
    #test_5()
    #test_6()