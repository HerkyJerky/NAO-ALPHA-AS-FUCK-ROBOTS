__author__ = 'redsphinx'

from SLAM import SLAM


class SLAMControl(SLAM):
    def __init__(self):
        SLAM.__init__()


    def reset(self):

        pass

    def run_slam(self):

        pass

    def send_measurement_data(self, measurement_data, time_step):

        pass

    def send_motion_data(self, motion_data, time_step):

        pass

    def set_parameter(self, parameter_name, value):

        pass



