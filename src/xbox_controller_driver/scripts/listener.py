#usr/bin/env python

import rospy
from xbox_controller_driver.msg import Tank


def callback(data):
    rospy.loginfo(rospy.get_caller_id())
    print(data.powerLevel)
    print(data.angle)
def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("controller",Tank, callback)
    
    rospy.spin()


if __name__=='__main__':
    listener()
    
