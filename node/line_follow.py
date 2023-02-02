#! /usr/bin/env python3

import rospy
import cv2 as cv
import numpy as np 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError



def callback(data):
    try:
        image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    rate = rospy.Rate(2)
    move = Twist()

    shape = image.shape
    h = shape[0]
    w = shape[1]
    
    #make grey scale
    gray_frame = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    #make binary
    threshold = 90 #@param {type: "slider", min : 0, max : 255}
    _, img_bin = cv.threshold(gray_frame, threshold, 255, 0)

    #use contours
    # contours, hierarchy = cv.findContours(img_bin, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # contour_color = (0, 0, 255)
    # contour_thick = 5
    # with_contours = cv.drawContours(img_bin, contours, -1, contour_color, contour_thick)


    #fixed y height at the bottom
    fixed_height = img_bin[600, :]
    y2 = img_bin[680,:] #added another height

    total_x = 0
    val = 0
    indexes = 0

    for i in range(len(fixed_height)):
        val = fixed_height[i]
        print(val)
        if val == 0:
            total_x = total_x + i
            indexes = indexes + 1

    if indexes != 0:
        centre = int(total_x/indexes) #centre x position
    else:
        centre = 0
    
    print(total_x, indexes, centre)

    if centre < w/2:
        rate = rospy.Rate(2)
        move = Twist()
        move.linear.x = 0.1
        move.angular.z = 0.5
    elif centre > w/2:
        rate = rospy.Rate(2)
        move = Twist()
        move.linear.x = 0.1
        move.angular.z = -0.5
    else:
        centre = 0
        rate = rospy.Rate(2)
        move = Twist()
        move.linear.x = 0.25
        move.angular.z = 0.5

    total_x = 0
    indexes = 0
    for i in range(len(y2)):
        val = y2[i]
        print(val)
        if val == 0:
            total_x = total_x + i
            indexes = indexes + 1
    if indexes != 0:
        centre = int(total_x/indexes)
    else:
        centre = 0

    if centre < w/2:
        rate = rospy.Rate(2)
        move = Twist()
        move.linear.x = 0.1
        move.angular.z = 0.5
    elif centre > w/2:
        rate = rospy.Rate(2)
        move = Twist()
        move.linear.x = 0.1
        move.angular.z = -0.5
    else:
        centre = 0
        rate = rospy.Rate(2)
        move = Twist()
        move.linear.x = 0.25
        move.angular.z = 0.5

        #input from TA:
        #Can implement PID to adjust the angular velocity (w) when the robot moves

    

    cv.imshow("Image window", img_bin)
    cv.waitKey(3)
        
    move_pub.publish(move)

    #cmd_vel_pub.publish()

    return None

    

#create object
bridge = CvBridge()
image_sub = rospy.Subscriber("/rrbot/camera1/image_raw", Image, callback) #subscribe calls the callback func like an interrupt
move_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1) 

rospy.init_node('image_converter', anonymous = True)

try:
    rospy.spin() #it makes it go on an endless loop instead of just going once
except KeyboardInterrupt:
    print("Shut down")
cv.destroyAlllWindows()
