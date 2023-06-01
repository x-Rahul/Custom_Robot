#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import cv2 as cv

class ObjectTrack(object):

    def __init__(self):
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.clbck)
        self.bridge_object = CvBridge()
        
    def clbck(self, data):
        try:
            cv_img = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)

        height, width, channels = cv_img.shape
        descentre = 160
        rows_to_watch=100
        crop_img = cv_img[int((height)/2+descentre):int((height)/2+(descentre+rows_to_watch))][1:int(width)]

        # crop_img is image received 
        # open cv code here ---------
    
        cv.imshow('openCV Window', crop_img)
        print(type(crop_img))
        cv.waitKey(1)

        #---------

def main():
    object_track = ObjectTrack()
    rospy.init_node('camera_object_track', anonymous=True)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Keyboard Kill")

if __name__=='__main__':
    main()