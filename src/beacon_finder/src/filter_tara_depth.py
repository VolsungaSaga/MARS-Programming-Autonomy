#!usr/bin/env python
import rospy
import sys
#Anything else you need...


#Notes:
# Want to parameterize:
# - input image topic
# - output image topic
# Using the ROS parameter server




rospy.init_node("filter_tara_depth")

while not rospy.is_shutdown():
	pass
	#Convert the image to opencv image

	#Apply Gaussian filter

	#Go back to ROS image

	#Publish new image.