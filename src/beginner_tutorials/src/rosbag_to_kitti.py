#!usr/bin/env python 
# -*- coding: utf-8 -*-

# python3 rosbag_to_kitti.py --img0_topic=/camera/infra1/image_rect_raw --img1_topic=/camera/infra2/image_rect_raw --imu_topic=/camera/imu --img_color=/camera/color/image_raw --data_set_path=/home/nuc02/data_sets/indoor_1

import rospy
from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu

import os

import cv2
import cv_bridge
from cv_bridge import CvBridge
from cv_bridge.boost.cv_bridge_boost import getCvType

import glob

import numpy as np

import message_filters

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--img0_topic', help= "the topic of camera left")
parser.add_argument('--img1_topic', help= "the topic of camera right")
parser.add_argument('--imu_topic', help='the topic of imu')
parser.add_argument('--img_color', help='the topic of camera color')
parser.add_argument('--data_set_path', help='the path of data set want to write')

args = parser.parse_args()

image_0_path = args.data_set_path + "/image_0"
image_1_path = args.data_set_path + "/image_1"
image_color_path = args.data_set_path + "/color"
imu_dir_path = args.data_set_path + "/oxts"

image_time_path = args.data_set_path + "/times.txt"
image_color_time_path = args.data_set_path + "/times_color.txt"
imu_data_path = args.data_set_path + "/oxts/ImuData.txt"
imu_time_path = args.data_set_path + "/oxts/time.txt"

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        print("---  创建新的文件夹...  ---")
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  OK  ---")
    else:
        print("---  文件夹已存在!  ---")

def touchDoc(path):
    Doc = os.path.exists(path)
    if not Doc: #如果不存在该文件，则直接创建
        print("---  创建新的文件...  ---")
        file = open(path, 'w') # makedirs 创建文件时如果路径不存在会创建这个路径
        file.close()
        print("---  OK  ---")
    else: 
        print ("清空内容")
        file = open(path, 'w')
        file.close()


def make_data_set_dir_struct():
    mkdir(image_0_path)
    mkdir(image_1_path)
    mkdir(image_color_path)
    mkdir(imu_dir_path)

    touchDoc(image_time_path)
    touchDoc(image_color_time_path)
    touchDoc(imu_data_path)
    touchDoc(imu_time_path)

gray_num = 0
color_num = 0

#cv_bridge
bridge = CvBridge()
bridge_color = CvBridge()

def callback_stereo_gray(img_left, img_right):
    time1 = img_left.header.stamp.to_sec()
    time2 = img_right.header.stamp.to_sec()

    file = open(image_time_path,'a')
    file.write(str(time1)+ '\n')
    file.close()

    delta_time = abs(time1 - time2)

    rospy.loginfo(delta_time)
    global gray_num
    png_name = str(gray_num)
    png_name = png_name.zfill(6)
    png_name = png_name + ".png"
    gray_num = gray_num + 1
    left_path = image_0_path + "/" + png_name
    right_path = image_1_path + "/" + png_name

    cv_image_left = bridge.imgmsg_to_cv2(img_left)
    cv_image_right = bridge.imgmsg_to_cv2(img_right)
    cv2.imwrite(left_path, cv_image_left)
    cv2.imwrite(right_path, cv_image_right)
    # print(img_left.header.stamp.to_sec())
    # print(img_right.header.stamp.to_sec())

def callback_imu_data(Imu_data):
    imu_time = Imu_data.header.stamp.to_sec()

    file = open(imu_time_path,'a')
    file.write(str(imu_time)+ '\n')
    file.close()

    file_imu = open(imu_data_path, 'a')
    file_imu.write(str(Imu_data.linear_acceleration.x) + ' ')
    file_imu.write(str(Imu_data.linear_acceleration.y) + ' ')
    file_imu.write(str(Imu_data.linear_acceleration.z) + ' ')
    file_imu.write(str(Imu_data.angular_velocity.x) + ' ')
    file_imu.write(str(Imu_data.angular_velocity.y) + ' ')
    file_imu.write(str(Imu_data.angular_velocity.z) + ' ')
    file_imu.write('\n')
    file_imu.close()

def callback_image_color(img_color):
    time1 = img_color.header.stamp.to_sec()
    file = open(image_color_time_path,'a')
    file.write(str(time1)+ '\n')
    file.close()

    global color_num
    png_name = str(color_num)
    png_name = png_name.zfill(6)
    png_name = png_name + ".png"
    color_num = color_num + 1
    color_path = image_color_path + "/" + png_name

    color_img = bridge_color.imgmsg_to_cv2(img_color)
    cv2.imwrite(color_path, color_img)










make_data_set_dir_struct()

rospy.init_node('lis_2_talkers', anonymous=True)

gray_camera_left = message_filters.Subscriber(args.img0_topic, Image)
gray_camera_right = message_filters.Subscriber(args.img1_topic, Image)

ts_stereo = message_filters.ApproximateTimeSynchronizer([gray_camera_left, gray_camera_right], 10, 0.01)

ts_stereo.registerCallback(callback_stereo_gray)

rospy.Subscriber(args.imu_topic, Imu, callback_imu_data, queue_size=10)
rospy.Subscriber(args.img_color, Image, callback_image_color,queue_size=10)


rospy.spin()