#!/usr/bin/env python
from __future__ import print_function
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
import rospy
import sys
import roslib
roslib.load_manifest('beacon_finder')


class image_converter:

    def __init__(self):
        self.image_pub = rospy.Publisher("depth_filtered", Image)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/taraxl/depth/image", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data)
        except CvBridgeError as e:
            pass

        # if cols > 60 and rows > 60:
        #     cv2.circle(cv_image, (50, 50), 10, 255)
        cv2.GaussianBlur(cv_image, (7, 7), 0)
        #cv2.imshow("Image window", cv_image)
        #cv2.waitKey(3)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image))
        except CvBridgeError as e:
            print(e)


def main(args):
    rospy.init_node('image_converter', anonymous=True)
    ic = image_converter()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    #cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
