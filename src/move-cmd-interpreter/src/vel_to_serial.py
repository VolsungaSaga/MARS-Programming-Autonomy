#!/usr/bin/env python

import rospy
import sys
import numpy as np
import serial

from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import UInt8MultiArray #Has a lot of data overhead. Might wanna define our own lightweight version.


class SerialSender():
    def __init__(self, port):
        rospy.init_node("serial_sender")
        self.ser = serial.Serial(port = port, baudrate=115200, timeout=1)
        self.usedPort = port
    
        self.talon_cmd_offest = 127     
        self.gamepadVelCmdSub = rospy.Subscriber("/game_cmd_vel", Twist, self.gameCmdCallback)
        
        self.autoVelCmdSub = rospy.Subscriber("/auto_cmd_vel", Twist, self.velCmdCallback)
    
           


    def send_serial_pkg(self,ser, values):
        packet = [255,255] 
        packet.extend([value + self.talon_cmd_offset for value in values])
        packet.append(sum(values) % 255)
        ser.write(bytearray(pkg))
        ser.flush()
        
    def read_serial_pkg(self,ser, chars = 10):
        ser.flush()
        pkg_recv = ser.read(chars)

        return pkg_recv
        
        
    ''' This function will convert linear/angular vels from Twist
    to the array of motor commands. '''
    def velCmdCallback(self,data):
        #TODO
        pass
    '''
    This function is meant to take in values from 0 - 100.
    0 is full reverse, 100 is full forward. It will send these values directly on the serial line with only minimal manipulation.
    '''
    def gameCmdCallback(self,data):
        #All we do is shove the data through the serial line.
        self.send_serial_pkg(self.ser, data.data)
        
        
        
if __name__ == "__main__":
    port = "/dev/ttyS0"
    if len(sys.argv) == 2:
        port = sys.argv[1]

    serSender = SerialSender(port)
    while not rospy.is_shutdown():
        test_pkg = [1, 2]
        rospy.loginfo("Sending {} on port {}".format(test_pkg, port))
        serSender.send_serial_pkg(serSender.ser, test_pkg)
        test_rcv = serSender.read_serial_pkg(serSender.ser, 10)
        rospy.loginfo("Received: {}".format(test_rcv))
        break
        #rospy.spin()
    #Close the serial port after ROS is shut down.    
    serSender.ser.close()
    
