#!/usr/bin/env python3
import rospy
import cv2 as cv
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

bridge = CvBridge()

def img_clbck(img_msg):
    try:
        img_cv = bridge.imgmsg_to_cv2(img_msg, "bgr8")
        cv.imshow("Image Raw window", img_cv)
        cv.waitKey(3)
    except CvBridgeError as e:
        print(e)

def main():
    print("hello")
    rospy.init_node('img_node')
    img_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, img_clbck)
    rospy.spin()

if __name__=='__main__':
    main()
