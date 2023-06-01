#! /usr/bin/env python3

# import ros stuff
import rospy
# import ros message
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
# import ros service
from std_srvs.srv import *

import math

srv_client_camera_control_ = None
srv_client_stop = None

yaw_ = 0
yaw_error_allowed_ = 5 * (math.pi / 180) # 5 degrees

regions_ = None
state_desc_ = ['Camera Control', 'Stop']
state_ = 0

# 0 - camera control
# 1 - stop

# callbacks
bridge = CvBridge()
def img_clbck(img_msg):
    img_cv = bridge.imgmsg_to_cv2(img_msg, "bgr8")
  


def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }


def change_state(state):
    global state_, state_desc_
    global srv_client_stop, srv_client_camera_control_
    state_ = state
    log = "state changed: %s" % state_desc_[state]
    rospy.loginfo(log)
    if state_ == 0:
        resp = srv_client_camera_control_(True)
        resp = srv_client_stop(False)
    if state_ == 1:
        resp = srv_client_camera_control_(False)
        resp = srv_client_stop(True)


def main():
    global regions, state_, yaw_, yaw_error_allowed_
    global srv_client_camera_control_, srv_client_stop
    
    rospy.init_node('main0')
    
    sub_laser = rospy.Subscriber('/laser/scan', LaserScan, clbk_laser)
    img_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, img_clbck)
    
    rospy.wait_for_service('/camera_control_switch')
    rospy.wait_for_service('/stop_switch')
    rospy.wait_for_service('/gazebo/set_model_state')
    
    srv_client_camera_control_ = rospy.ServiceProxy('/camera_control_switch', SetBool)
    srv_client_stop = rospy.ServiceProxy('/stop_switch', SetBool)
    # srv_client_set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    
    # # set robot position
    # model_state = ModelState()
    # model_state.model_name = 'rahul_bot'
    # model_state.pose.position.x = initial_position_.x
    # model_state.pose.position.y = initial_position_.y
    # resp = srv_client_set_model_state(model_state)
    
    # initialize camera control
    change_state(0)
    rate = rospy.Rate(20)

    while not rospy.is_shutdown():
        if regions_ == None:
            continue
        
        if state_ == 0:
            if regions_['front'] > 0.15 and regions_['front'] < 1:
                change_state(1)
        
        rate.sleep()

if __name__ == "__main__":
    main()
