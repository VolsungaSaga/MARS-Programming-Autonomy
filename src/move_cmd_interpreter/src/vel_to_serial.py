#!/usr/bin/env python

import rospy
import sys
import numpy as np
import serial

from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import UInt8MultiArray #Has a lot of data overhead. Might wanna define our own lightweight version.
from xbox_controller_driver.msg import ControllerState

class SerialSender():
    def __init__(self, port):
        rospy.init_node("serial_sender")
        self.ser = serial.Serial(port = port, baudrate=115200, timeout=1)
        self.usedPort = port
    
        self.talon_cmd_offest = 127     
        #self.gamepadVelCmdSub = rospy.Subscriber("/game_cmd_vel", Twist, self.gameCmdCallback)

        self.gamepadStateSub = rospy.Subscriber("/controller", ControllerState, self.gameCmdCallback)
        
        self.autoVelCmdSub = rospy.Subscriber("/auto_cmd_vel", Twist, self.velCmdCallback)
    
           
    def normalize(x, xmin, xmax, a, b):
        return a + (x - xmin) * (b-a)/(xmax - xmin)

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
    This function is meant to directly interpret the gamepad state into motor outputs.
    0 is full reverse, 100 is full forward. It will send these values directly on the serial line with only minimal manipulation.
    '''
    def gameCmdCallback(self,data):
        #All we do is shove the data through the serial line.
        left_motor = int(self.normalize(data.normalizeLeftY, 0., 1., 0., 100.))
        right_motor = int(self.normalize(data.normalizeRightY, 0., 1., 0., 100.))
	
	'''
	TODO: Fill these in!
	A:
	B:
	X:
	Y:
	Left Bumper:
	Left Trigger:
	
	''' 
	button_A = int(self.normalize(data.A, 0, 1, 0, 100))
	button_B = int(self.normalize(data.B, 0, 1, 0, 100))
	button_X = int(self.normalize(data.X, 0, 1, 0, 100))
	button_Y = int(self.normalize(data.Y, 0, 1, 0, 100))

	bump_left = int(self.normalize(data.leftBumper, 0, 1, 0, 100))
	trigger_left = int(self.normalize(data.leftTrigger, 0., 1., 0., 100.))
        self.send_serial_pkg(self.ser, [left_motor, right_motor, button_A, button_B, button_X, button_Y, bump_left, trigger_left])
        
        
        
if __name__ == "__main__":
    port = "/dev/ttyS0"
    if len(sys.argv) == 2:
        port = sys.argv[1]

    serSender = SerialSender(port)
    while not rospy.is_shutdown():
        rospy.spin()

    #Close the serial port after ROS is shut down.    
    serSender.ser.close()
    
