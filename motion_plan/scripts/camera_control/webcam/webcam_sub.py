#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import Float32MultiArray
import cv2 as cv


pub = None


def clbck(msg):
    # rospy.loginfo(rospy.get_caller_id() + " Data Received : %s", msg.data)

    cx,cy,W,H = msg.data[0],msg.data[1],msg.data[2],msg.data[3]
    
    err_x = cx-W/2
    speed_cmd = Twist()
    speed_cmd.linear.x = 0.4
    speed_cmd.angular.z = -err_x/100;
    pub.publish(speed_cmd)
    print("Tracking")
    #------------
    

def main():
    global pub
    rospy.init_node('webcam_sub_and_pub', anonymous=False)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub = rospy.Subscriber('/obj_cord', Float32MultiArray, clbck)
    rospy.spin()

    
if __name__=='__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass