import numpy as np
import time
import rospy
import message_filters
import math
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu
from imu_kalman_filter.msg import AccelYaw
x = np.array([0,0,0,0]).transpose()
A = np.identity(4)
Q = np.identity(4)*0.01#needs to be finetuned
R = np.identity(12)*0.04#linear_acceleration_data data taken from imu_node.py from razor_ros_9d0f
R[11][11],R[10][10],R[9][9] = 0.0025,0.0025,0.0025 #orientation covariance data
C = np.zeros((12,4))
P = np.identity(4)
C[0][0],C[1][0],C[2][0],C[3][1],C[4][1],C[5][1],C[6][2],C[7][2],C[8][2],C[9][3],C[10][3],C[11][3] = 1,1,1,1,1,1,1,1,1,1,1,1

#z = np.array([imuOne[0],imuTwo[0],imuThree[0],imuOne[1],imuTwo[1],imuThree[1],imuOne[2],imuTwo[2],imuThree[2]]).transpose()
qSize = 10
pub = rospy.Publisher('imuKalman', AccelYaw, queue_size=qSize)
rospy.init_node('imuKalman', anonymous=True)
rate = rospy.Rate(10) # 10hz
seq = 0
def Kalman(z):
	global x,A,Q,R,C,P,seq
	#time update
	x = np.matmul(A,x)
	P = np.matmul(A,np.matmul(P,A.transpose()))+Q
	#measurement update
	K = np.matmul(np.matmul(P,C.transpose()), np.linalg.inv(np.matmul(C,np.matmul(P,C.transpose()))+R))
	x = x+np.matmul(K,(z-np.matmul(C,x)))
	P = np.matmul((np.identity(4)-np.matmul(K,C)),P)
	
	accelYawMsg = AccelYaw()
	accelYawMsg.linear_acceleration_x = x[0]
	accelYawMsg.linear_acceleration_y = x[1]
	accelYawMsg.linear_acceleration_z = x[2]
	accelYawMsg.yaw = x[3]
	seq = seq+1
	accelYawMsg.header.seq = seq
	accelYawMsg.header.stamp= rospy.Time.now()
	accelYawMsg.header.frame_id = 'imu_Kalman'
	pub.publish(accelYawMsg)
	

def getYaw(qx,qy,qz,qw):
	return math.atan2(2.0*(qy*qz + qw*qx), qw*qw - qx*qx - qy*qy + qz*qz); # formula needs to be verified maybe use code below
	#siny_cosp = 2.0 * (qw * qz + qx * qy);
	#cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz);  
	#yaw = atan2(siny_cosp, cosy_cosp);
	#return yaw

def callback(imu1,imu2,imu3):
	yaw1 = getYaw(imu1.orientation.x,imu1.orientation.y,imu1.orientation.z,imu1.orientation.w)
	yaw2 = getYaw(imu1.orientation.x,imu1.orientation.y,imu1.orientation.z,imu1.orientation.w)
	yaw3 = getYaw(imu1.orientation.x,imu1.orientation.y,imu1.orientation.z,imu1.orientation.w)
	#rospy.loginfo(rospy.get_caller_id() + 'I heard %s', imu2.linear_acceleration)
	z = np.array([imu1.linear_acceleration.x,imu2.linear_acceleration.x,imu3.linear_acceleration.x,imu1.linear_acceleration.y,imu2.linear_acceleration.y,imu3.linear_acceleration.y,imu1.linear_acceleration.z,imu2.linear_acceleration.z,imu3.linear_acceleration.z,yaw1,yaw2,yaw3]) 
	#update global variables
	#run Kalman filter code
	Kalman(z)

def start():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
	

	#rospy.Subscriber('imu1', Imu, callback)
    #rospy.Subscriber('imu2', Imu, callback)
    #rospy.Subscriber('imu3', Imu, callback)
	imu1 = message_filters.Subscriber('imu1', Imu)
	imu2 = message_filters.Subscriber('imu2', Imu)
	imu3 = message_filters.Subscriber('imu3', Imu)
	
	#ts = message_filters.TimeSynchronizer([imu1, imu2, imu3], qSize) #not sure what the queue_size of 10 does. Also, might have to use Approximate Time Synch message filter if the IMU's are not synchronized well
	ts = message_filters.ApproximateTimeSynchronizer([imu1, imu2, imu3], qSize, 0.09) #rate is 0.1s, so slop is set to 0.09s
	ts.registerCallback(callback)

    # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
    


if __name__ == '__main__':
    start()
