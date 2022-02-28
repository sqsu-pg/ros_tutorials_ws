#!usr/bin/env python 
# -*- coding: utf-8 -*-

import rospy 
from sensor_msgs.msg import Image

import os
import sys
# sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')
# sys.path.append('/home/liubo/anaconda3/envs/grad_deep_learn/lib/python3.6/site-packages')
import cv2
import cv_bridge
print (cv_bridge.__path__)
from cv_bridge import CvBridge
from cv_bridge.boost.cv_bridge_boost import getCvType
import glob

import numpy as np


# sys.path.append('/opt/ros/melodic/lib/python2.7/dist-packages')


def get_times(time_txt):
    times_vec = []
    with open(time_txt, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            # print(float(line))
            times_vec.append(float(line))
    return times_vec




def talker():
    pub_left = rospy.Publisher('left_cam', Image, queue_size=5)

    pub_right = rospy.Publisher('right_cam', Image, queue_size=5)

    rospy.init_node('talk_image', anonymous=True)
    
    rate = rospy.Rate(1)

    bridge1 = CvBridge()
    bridge2 = CvBridge()

    data_set_path = "/home/liubo/data_sets/04"
    data_set_time_txt = data_set_path + '/times.txt'

    times_vec = get_times(data_set_time_txt)

    left_path = glob.glob(os.path.join(data_set_path + '/image_0/', '*.png'))
    left_path = sorted(left_path)
    # print (left_path)
    right_path = glob.glob(os.path.join(data_set_path + '/image_1/', '*.png'))
    right_path = sorted(right_path)
    
    count = 0
    while not rospy.is_shutdown():
        # left_img = Image()
        # right_img = Image()
        ImageLeft = cv2.imread(left_path[count])
        print (type(ImageLeft))
        print("ImageLeft shape : ", ImageLeft.shape)
        print (count)
        ImageRight = cv2.imread(right_path[count])

        left_img = bridge1.cv2_to_imgmsg(ImageLeft)
        left_img.header.stamp.secs = times_vec[count]
        print (left_img.height)
        print (left_img.width)
        print (left_img.step)
        right_img = bridge2.cv2_to_imgmsg(ImageRight)
        right_img.header.stamp.secs = times_vec[count]

        pub_left.publish(left_img)
        pub_right.publish(right_img)
        count += 1


        rate.sleep()



if __name__ == '__main__':
    # times_txt = "/home/liubo/data_sets/04/times.txt"
    # get_times(times_txt)
    try:
        talker()
    except rospy.ROSInternalException:
        pass