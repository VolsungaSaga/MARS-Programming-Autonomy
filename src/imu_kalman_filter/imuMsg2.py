import rospy
import serial
import string
import math
import sys

#from time import time
from sensor_msgs.msg import Imu

pub = rospy.Publisher('imu2', Imu, queue_size=1)
rospy.init_node('imuTalker', anonymous=True)
diag_pub_time = rospy.get_time();
rate = rospy.Rate(10) # 10hz

imuMsg = Imu()

while not rospy.is_shutdown():
	imuMsg.orientation_covariance = [
	0.0025 , 0 , 0,
	0, 0.0025, 0,
	0, 0, 0.0025
	]
	
	imuMsg.angular_velocity_covariance = [
	0.02, 0 , 0,
	0 , 0.02, 0,
	0 , 0 , 0.02
	]

	imuMsg.linear_acceleration_covariance = [
	0.04 , 0 , 0,
	0 , 0.04, 0,
	0 , 0 , 0.04
	]

	imuMsg.linear_acceleration.x = 3.0
	imuMsg.linear_acceleration.y = 4.0
	imuMsg.linear_acceleration.z = 5.0

	imuMsg.angular_velocity.x = 6.0
	imuMsg.angular_velocity.y = 7.0
	imuMsg.angular_velocity.z = 8.0

	imuMsg.orientation.x = 9.0
	imuMsg.orientation.y = 10.0
	imuMsg.orientation.z = 11.0
	imuMsg.orientation.w = 12.0
	imuMsg.header.stamp= rospy.Time.now()
	imuMsg.header.frame_id = 'base_imu_link'
	imuMsg.header.seq = 13
	pub.publish(imuMsg)
	rate.sleep()
