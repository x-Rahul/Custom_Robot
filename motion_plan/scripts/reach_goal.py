#! /usr/bin/env python3

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations

import math

# robot state variables
position_ = Point()
yaw_ = 0
# machine state
state_ = 0

#     0: 'Fix Yaw'
#     1: 'Go Straight'
#     2: 'Stop'


# goal
goal_ = Point()
goal_.x = 6
goal_.y = 7
goal_.z = 0
# parameters
yaw_precision_ = math.pi / 90 # +/- 2 degree allowed
dist_precision_ = 0.3

# publishers
pub = None

# callbacks
def clbk_odom(msg):
    global position_
    global yaw_
    
    # position
    position_ = msg.pose.pose.position
    
    # yaw
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]
    # roll = euler[0]
    # pitch = euler[1]  

def change_state(state):
    global state_
    state_ = state
    print ('State changed to [%s]' % state_) 

def normalize_angle(angle):
    if(math.fabs(angle) > math.pi):
        angle = angle - (2 * math.pi * angle) / (math.fabs(angle)) # fabs -> absolute float point
    return angle

def fix_yaw(gol_):
    global yaw_, pub, yaw_precision_, state_
    desired_yaw = math.atan2(gol_.y - position_.y, gol_.x - position_.x) # How much to rotate about z to get to goal point. invtan()-> angle in rads
    err_yaw = normalize_angle(desired_yaw - yaw_)
    
    rospy.loginfo(err_yaw)
    
    twist_msg = Twist()
    if math.fabs(err_yaw) > yaw_precision_:
        twist_msg.angular.z = 0.7 if err_yaw > 0 else -0.7 # if yaw_error > 0 then turn left(+) else right(-)
    
    pub.publish(twist_msg)
    
    # state change conditions
    if math.fabs(err_yaw) <= yaw_precision_: 
        print ('Yaw error: [%s]' % err_yaw) 
        change_state(1) # Go Straight

def go_straight_ahead(gol_):
    global yaw_, pub, yaw_precision_, state_
    desired_yaw = math.atan2(gol_.y - position_.y, gol_.x - position_.x)
    err_yaw = desired_yaw - yaw_
    err_pos = math.sqrt(pow(gol_.y - position_.y, 2) + pow(gol_.x - position_.x, 2))
    
    if err_pos > dist_precision_:
        twist_msg = Twist()
        twist_msg.linear.x = 0.6
        twist_msg.angular.z = 0.2 if err_yaw > 0 else -0.2
        pub.publish(twist_msg)
    else:
        print ('Position error: [%s]' % err_pos) 
        change_state(2)
    
    # state change conditions
    if math.fabs(err_yaw) > yaw_precision_:
        print ('Yaw error: [%s]' % err_yaw) #...............
        change_state(0)

def done():
    twist_msg = Twist()
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    pub.publish(twist_msg)

def main():
    global pub
    
    rospy.init_node('go_to_point')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom) # odometry: to know posn of robot 
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if state_ == 0: 
            fix_yaw(goal_)
        elif state_ == 1:
            go_straight_ahead(goal_)
        elif state_ == 2:
            done() 
            pass
        else:
            rospy.logerr('Unknown state!')
            pass
        rate.sleep()

if __name__ == '__main__':
    main()
