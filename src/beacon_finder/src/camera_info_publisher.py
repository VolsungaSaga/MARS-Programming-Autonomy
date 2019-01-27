#!/usr/bin/env python

#This script is meant to publish the intrinsic camera matrix for the TaraXL, since that see3cam package is having issues
# with libv4l2.

#General Params
distortion_model = "plumb_bob"

#TARAXL LEFT CAMERA INFO:

"""
pointgrey_camera_driver (at least the version installed with apt-get) doesn't
properly handle camera info in indigo.
This node is a work-around that will read in a camera calibration .yaml
file (as created by the cameracalibrator.py in the camera_calibration pkg),
convert it to a valid sensor_msgs/CameraInfo message, and publish it on a
topic.

The yaml parsing is courtesy ROS-user Stephan:
    http://answers.ros.org/question/33929/camera-calibration-parser-in-python/

This file just extends that parser into a rosnode.
"""
import rospy
import yaml
from sensor_msgs.msg import CameraInfo

def yaml_to_CameraInfo(yaml_fname):
    """
    Parse a yaml file containing camera calibration data (as produced by 
    rosrun camera_calibration cameracalibrator.py) into a 
    sensor_msgs/CameraInfo msg.
    
    Parameters
    ----------
    yaml_fname : str
        Path to yaml file containing camera calibration data

    Returns
    -------
    camera_info_msg : sensor_msgs.msg.CameraInfo
        A sensor_msgs.msg.CameraInfo message containing the camera calibration
        data
    """
    # Load data from file
    with open(yaml_fname, "r") as file_handle:
        calib_data = yaml.load(file_handle)
    # Parse
    camera_info_msg = CameraInfo()
    camera_info_msg.width = calib_data["image_width"]
    camera_info_msg.height = calib_data["image_height"]
    camera_info_msg.K = calib_data["camera_matrix"]["data"]
    camera_info_msg.D = calib_data["distortion_coefficients"]["data"]
    camera_info_msg.R = calib_data["rectification_matrix"]["data"]
    camera_info_msg.P = calib_data["projection_matrix"]["data"]
    camera_info_msg.distortion_model = calib_data["distortion_model"]
    return camera_info_msg


def get_cam_info_left():
    cam_info = CameraInfo()
    cam_info.width = 752
    cam_info.height = 480
    cam_info.K = [ 7.1623767806883029e+002, 0., 3.8077949374262056e+002, 0.,
       7.1623767806883029e+002, 2.1786685878818076e+002, 0., 0., 1. ]
    cam_info.D = [ 7.5142546188962184e-002, -9.3787546047981382e-002,
       1.6692040534575499e-003, -4.0889004262752079e-004]
    cam_info.R = [9.9863313595266778e-001, -3.6214326873450909e-003,
       -5.2141586115417193e-002, 3.6833309798456879e-003,
       9.9999262128647204e-001, 1.0910753884294238e-003,
       5.2137250121514329e-002, -1.2816387561852772e-003,
       9.9863910626004693e-001]
    cam_info.P = [ 7.6560556152317668e+002, 0., 4.2582975387573242e+002, 0., 0.,
       7.6560556152317668e+002, 2.2225554084777832e+002, 0., 0., 0., 1.,
       0. ]
    cam_info.distortion_model = "equidistant"
    return cam_info
    
def get_cam_info_right():
    cam_info = CameraInfo()
    cam_info.width = 752
    cam_info.height = 480
    cam_info.K = [ 7.1623767806883029e+002, 0., 3.7952224231819093e+002, 0.,
       7.1623767806883029e+002, 2.2665882878276798e+002, 0., 0., 1. ]
    cam_info.D = [ 7.0940303672828275e-002, -8.3481074716348150e-002,
       -3.0675339642308669e-003, 1.0042332230591974e-00]
    cam_info.R = [ 9.9884162841721502e-001, -5.3589610059405256e-003,
       -4.7819273078780991e-002, 5.3129464379608748e-003,
       9.9998529289134919e-001, -1.0893122370687993e-003,
       4.7824407377337952e-002, 8.3398917215879236e-004,
       9.9885541021764856e-001 ]
    cam_info.P = [ 7.6560556152317668e+002, 0., 4.2582975387573242e+002,
       -4.6009434918815954e+004, 0., 7.6560556152317668e+002,
       2.2225554084777832e+002, 0., 0., 0., 1., 0. ]
    cam_info.distortion_model = "equidistant"
    return cam_info

if __name__ == "__main__":
    # Get fname from command line (cmd line input required)
    #import argparse
    #arg_parser = argparse.ArgumentParser()
    #arg_parser.add_argument("filename", help="Path to yaml file containing " +\
    #                                         "camera calibration data")
    #args = arg_parser.parse_args()
    #filename = args.filename

    # Parse yaml file
    #camera_info_msg = yaml_to_CameraInfo(filename)
    
    cam_info_left = get_cam_info_left()
    cam_info_right = get_cam_info_right()
    
    # Initialize publisher node
    rospy.init_node("camera_info_publisher", anonymous=True)
    publisher1 = rospy.Publisher("/taraxl/left/camera_info", CameraInfo, queue_size=10)
    #rate = rospy.Rate(10)
    
    rospy.init_node("camera_info_publisher", anonymous=True)
    publisher2 = rospy.Publisher("/taraxl/right/camera_info", CameraInfo, queue_size=10)
    rate = rospy.Rate(10)

    
    # Run publisher
    while not rospy.is_shutdown():
        publisher1.publish(cam_info_left)
        publisher2.publish(cam_info_right)
        rate.sleep()

