#!/usr/bin/env python

import rospy,copy,math
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from pimouse_ros.msg import LightSensorValues

class WallTrace():
    def __init__(self):
        self.cmd_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback_sensors)
        self.sensors = LightSensorValues()

    def callback_sensors(self,messages):
        self.sensors = messages

    def run(self):
        rate = rospy.Rate(10)
        d = Twist()

        accel = 0.02
        data.linear.x = 0.0
        data.angular.z = 0
        while not rospy.is_shutdown():
            data.linear.x += accel

            if self.sensor_values.sum_forward > 50:
                data.linear.x = 0.0
            elif data.linear.x <= 0.2:
                data.linear.x = 0.2
            elif data.linear.x >= 0.8:
                data.linear.x = 0.8

            if data.linear.x < 0.2:
                data.angular.z = 0.0
            elif self.sensor_values.left_side < 10:
                data.angular.z = 0.0
            else:
                target = 50
          
                error = (target - self.sensor_values.left_side)/50.0
               
                data.angular.z = error * 3 * math.pi / 180.0

            self.cmd_vel.publish(data)
            rate.sleep()
        


if __name__ == '__main__':
    rospy.init_node('wall_trace')
    rospy.wait_for_service('/motor_on')
    rospy.wait_for_service('/motor_off')

    rospy.on_shutdown(rospy.ServiceProxy('/motor_off',Trigger).call)
    if not rospy.ServiceProxy('/motor_on',Trigger).call().success:
        rospy.logerr("motors are not empowered")
        sys.exit(1)

    WallStop().run()