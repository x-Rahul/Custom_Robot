#!/usr/bin/env python3

import cv2 as cv

cap = cv.VideoCapture(1)
print(cap.isOpened())

if not cap.isOpened():
    print("Cannot open camera")


while True:
    ret, img = cap.read()
    if not ret: break
    cv.imshow("Window", img)
    print(type(img))
    cv.waitKey(1)

