#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

from beginner_tutorials.msg import Num


def talker():
    ##queue_size 表示队列的大小，如果消息队列处理不够快，就会丢弃旧的消息
    pub = rospy.Publisher('chatter', String, queue_size= 10)
    
    pub_my = rospy.Publisher('my_msg', Num, queue_size = 10)
    ##初始化节点，开始跟rosmaster通讯，节点名字在网络中是唯一的，不能包含斜杠'/'
    rospy.init_node('talker', anonymous=True)

    ##创建Rate 对象，与sleep()函数结合使用，控制话题发布的频率
    rate = rospy.Rate(10) ##10Hz

    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        hello_my_msg = Num()
        hello_my_msg.last_name = 'george'
        hello_my_msg.first_name = 'paul'
        rospy.loginfo(hello_my_msg.first_name)

        pub.publish(hello_str)
        pub_my.publish(hello_my_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInternalException:
        pass
