#!/usr/bin/env python3
import rospy
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point, Twist
from std_srvs.srv import *

pub = None

# service callbacks
def camera_control_switch(req):
    global active_
    active_ = req.data
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res



#tracker = cv.TrackerMOSSE_create()
tracker = cv.TrackerCSRT_create() # High Accuracy Slow speed

count = 1
def opencv_code(img):
    global count
    if count == 1:
        bbox = cv.selectROI("Tracking", img, False)
        tracker.init(img, bbox)
        # cv.waitKey(3)
        count = count+1

    H,W,_ = img.shape
    ret, bbox = tracker.update(img)
    # print(bbox) # bbox coordinates [x,y,w,h]       
    center = (bbox[0]+bbox[2]//2, bbox[1]+bbox[3]//2)
    cx,cy = center[0],center[1]

    # print(center)
    if ret:
        cv.circle(img, center, 2, (0,255,0), 3)
    else:
        print("Not Found")

    cv.imshow("Tracking", img)
    cv.waitKey(1)

    err_x = cx-W/2
    speed_cmd = Twist()
    speed_cmd.linear.x = 0.4
    speed_cmd.angular.z = -err_x/200;
    pub.publish(speed_cmd)
    print("Tracking")

bridge = CvBridge()
def img_clbck(img_msg):
    img_cv = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    opencv_code(img_cv)

def main():
    global pub
    rospy.init_node('img_node')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    img_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, img_clbck)

    srv = rospy.Service('camera_control_switch', SetBool, camera_control_switch)

    rospy.spin()
    while not rospy.is_shutdown():
        print ("hello")

if __name__=='__main__':
    main()
