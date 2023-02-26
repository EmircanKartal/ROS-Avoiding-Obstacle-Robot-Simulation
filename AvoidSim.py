#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class RobotController:
    def __init__(self):
        rospy.init_node('robot_controller', anonymous=True)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.laser_callback)
        self.rate = rospy.Rate(10)
        self.vel = Twist()
        self.vel.linear.x = 0.0
        self.vel.angular.z = 0.0

    def laser_callback(self, data):
        if min(data.ranges) < 1.5:
            self.vel.linear.x = 0.0
            self.vel.angular.z = 0.5
        else:
            self.vel.linear.x = 0.3
            self.vel.angular.z = 0.0

    def run(self):
        while not rospy.is_shutdown():
            self.vel_pub.publish(self.vel)
            self.rate.sleep()

if __name__ == '__main__':
    controller = RobotController()
    try:
        controller.run()
    except rospy.ROSInterruptException:
        pass