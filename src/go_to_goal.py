#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
import numpy as np




def posecallback(data):
    global state
    state = np.array([data.x, data.y, data.theta])


def go_to_goal(x_des, vel_pub):
    global state
    rate = rospy.Rate(50)
    a = math.radians(x_des[2])
    x_des = np.array([x_des[0],x_des[1],a])
    vel_msg = Twist()
    flag = 0
    
    
   
    while True:
        if flag ==0:
            kp_angular = 1.5
            
            des_rot1 = math.atan2(x_des[1]-state[1],x_des[0]-state[0]) - state[2]
            angular_speed = kp_angular*des_rot1
            vel_msg.angular.z = angular_speed
            vel_pub.publish(vel_msg)
            rate.sleep()
           
            if abs(des_rot1) < 0.01:
                flag = 1
        if flag == 1:
            kp_linear = 2.0
            des_translation = abs(math.sqrt(((x_des[0]-state[0])**2)+((x_des[1]-state[1])**2)))
            linear_speed = kp_linear*des_translation
            vel_msg.linear.x = linear_speed
            vel_pub.publish(vel_msg)
            if des_translation < 0.03:
                flag = 2
            rate.sleep()
        if flag == 2:
            kp_angular = 1.5
            des_rot2 = x_des[2]-state[2]
            print(des_rot2)
            angular_speed = kp_angular*des_rot2
            print(angular_speed)
            vel_msg.angular.z = angular_speed
            vel_pub.publish(vel_msg)
           
            
            if abs(des_rot2) < 0.01:
                rospy.signal_shutdown()
                break
            rate.sleep()






rospy.init_node('turtlesim_gotogoal', anonymous=True)

vel_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
pose_sub = rospy.Subscriber("/turtle1/pose", Pose, posecallback)
time.sleep(1)
xdes = np.array([2, 2, 30])
go_to_goal(xdes, vel_pub)

