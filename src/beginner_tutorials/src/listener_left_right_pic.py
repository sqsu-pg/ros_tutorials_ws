import rospy 
from sensor_msgs.msg import Image

import os
import sys
sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')
sys.path.append('/home/liubo/anaconda3/envs/grad_deep_learn/lib/python3.6/site-packages')
import cv2
import cv_bridge
print (cv_bridge.__path__)
from cv_bridge import CvBridge
from cv_bridge.boost.cv_bridge_boost import getCvType
import glob

import numpy as np


# sys.path.append('/opt/ros/melodic/lib/python2.7/dist-packages')
# sys.path.remove('/home/liubo/anaconda3/envs/grad_deep_learn/lib/python3.6/site-packages')

bridge = CvBridge()


def callback(data):
    rospy.loginfo("I heard")

    Cv_Image_Left = bridge.imgmsg_to_cv2(data)

    print (type(Cv_Image_Left))
    print (Cv_Image_Left.shape)
    print (Cv_Image_Left.dtype)


if __name__ == '__main__':
    rospy.init_node("listener_left_right_pic", anonymous=True)

    rospy.Subscriber('/left_image', Image, callback, queue_size=5)

    rospy.spin()