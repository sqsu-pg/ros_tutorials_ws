#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import message_filters

from beginner_tutorials.msg import my_string 

def callback(talk_data1, talk_data2):

    time1 = talk_data1.header.stamp.to_sec()
    time2 = talk_data2.header.stamp.to_sec()

    delta_time = abs(time1 - time2)

    rospy.loginfo(delta_time)
    print(talk_data1.data)
    print(talk_data2.data)

    rospy.sleep(1)


rospy.init_node('lis_2_talkers', anonymous=True)

talk1_sub = message_filters.Subscriber('chatter1', my_string)
talk2_sub = message_filters.Subscriber('chatter2', my_string)

ts = message_filters.ApproximateTimeSynchronizer([talk1_sub, talk2_sub], 1, 0.1)

ts.registerCallback(callback)

rospy.spin()