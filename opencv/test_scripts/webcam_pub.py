#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32MultiArray
import cv2 as cv


def webcam():

    rospy.init_node('webcam_pub', anonymous=False)
    pub = rospy.Publisher('/obj_cord', Float32MultiArray, queue_size=1)
    rate = rospy.Rate(10)

    cap = cv.VideoCapture(1)
    print(cap.isOpened())

    #tracker = cv.TrackerMOSSE_create()
    tracker = cv.TrackerCSRT_create() # High Accuracy Slow speed

    ret, img = cap.read()
    img = cv.flip(img, 1)
    bbox = cv.selectROI("Tracking", img, False)
    tracker.init(img, bbox)

    while not rospy.is_shutdown():

        ret, img = cap.read()
        img = cv.flip(img, 1)
        H,W,_ = img.shape
        if not ret: break

        ret, bbox = tracker.update(img)
        # print(bbox) # bbox coordinates [x,y,w,h]       
        center = (bbox[0]+bbox[2]//2, bbox[1]+bbox[3]//2)
        cx,cy = center[0],center[1]

        print(center)
        msg = Float32MultiArray()
        msg.data = [cx, cy, W, H]
        pub.publish(msg)

        if ret:
            cv.circle(img, center, 2, (0,255,0), 3)
        else:
            print("Not Found")

        cv.imshow("Tracking", img)
        cv.waitKey(1)
        if rospy.is_shutdown(): cap.release()

if __name__=='__main__':
    try:
        webcam()
    except rospy.ROSInterruptException:
        pass