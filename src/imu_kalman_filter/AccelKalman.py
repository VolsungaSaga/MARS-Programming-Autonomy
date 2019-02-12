import numpy as np
import time
import rospy
from std_msgs.msg import Float64
imuOne = np.array([1,2,3])#needs to be replaced by interface with IMU
imuTwo = np.array([1,2,3])
imuThree = np.array([1,2,3])

x = np.array([0,0,0]).transpose()
A = np.identity(3)
Q = np.identity(3)*0#needs to be finetuned
R = np.identity(9)*0.03#needs to be finetuned, currently using tolerance from datasheet
C = np.zeros((9,3))
P = np.identity(3)
C[0][0],C[1][0],C[2][0],C[3][1],C[4][1],C[5][1],C[6][2],C[7][2],C[8][2] = 1,1,1,1,1,1,1,1,1

z = np.array([imuOne[0],imuTwo[0],imuThree[0],imuOne[1],imuTwo[1],imuThree[1],imuOne[2],imuTwo[2],imuThree[2]]).transpose()


pubX = rospy.Publisher('LinAccelX', Float64, queue_size=10Z)
pubY = rospy.Publisher('LinAccelY', Float64, queue_size=10)
pubZ = rospy.Publisher('LinAccelZ', Float64, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
	#time update
	x = np.matmul(A,x)
	P = np.matmul(A,np.matmul(P,A.transpose()))+Q
	#measurement update
	K = np.matmul(np.matmul(P,C.transpose()), np.linalg.inv(np.matmul(C,np.matmul(P,C.transpose()))+R))
	x = x+np.matmul(K,(z-np.matmul(C,x)))
	P = np.matmul((np.identity(3)-np.matmul(K,C)),P)
	time.sleep(0.1)
	print(x)

	pubX.publish(x[0])
	pubY.publish(x[1])
	pubZ.publish(x[2])
	rate.sleep()

