#!/usr/bin/env python3
import rospy
import cv2 as cv
import cvzone
from cvzone.ColorModule import ColorFinder

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point, Twist


bridge = CvBridge()
pub = None

count = 1
def opencv_code(img):
    global count
    if count == 1:
        H,W,_ = img.shape
        myColorFinder = ColorFinder(True)
        hsvVals = {'hmin': 33, 'smin': 72, 'vmin': 126, 'hmax': 58, 'smax': 255, 'vmax': 255}
        count +=1

    
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask) # filter =3 (tri),4 (sq,rect), 0 (auto)
    if contours:
        data = contours[0]['center'][0], \
               contours[0]['center'][1], \
               int(contours[0]['area'])
        print(data)

    imgStack = cvzone.stackImages([img, imgColor, mask, imgContour], 2, 0.5)
    cv.imshow("Image", imgStack)
    cv.waitKey(1)
    # err_x = cx-W/2
    # speed_cmd = Twist()
    # speed_cmd.linear.x = 0.4
    # speed_cmd.angular.z = -err_x/200;
    # pub.publish(speed_cmd)
    # print("Tracking")


def img_clbck(img_msg):
    img_cv = bridge.imgmsg_to_cv2(img_msg, "bgr8")
    opencv_code(img_cv)

def main():
    global pub
    rospy.init_node('img_node')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    img_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, img_clbck)
    rospy.spin()
    while not rospy.is_shutdown():
        print ("hello")

if __name__=='__main__':
    main()
