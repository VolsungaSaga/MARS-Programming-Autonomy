import rospy
import sensor_msg.CameraInfo


#This script is meant to publish the intrinsic camera matrix for the TaraXL, since that see3cam package is having issues
# with libv4l2.

#General Params
distortion_model = "plumb_bob"

#TARAXL LEFT CAMERA INFO:

#TARAXL RIGHT CAMERA INFO (Credit to Econ Systems for these parameters):
r_image_width = 640
r_image_height = 480
r_camera_name = cameraRight
r_camera_matrix = [732.426718, 0.000000, 329.908594, 0.000000, 730.192642, 256.639249, 0.000000, 0.000000, 1.000000] #3x3 matrix
r_distortion_coeffs = [0.067819, 0.034419, 0.015379, 0.008940, 0.000000] #1x5
 


def publish



if __name__ == "__main__":

	while(not rospy.is_shutdown()):
		 

