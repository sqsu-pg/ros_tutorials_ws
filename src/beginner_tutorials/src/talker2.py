#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

from beginner_tutorials.msg import my_string


def talker():
    ##queue_size 表示队列的大小，如果消息队列处理不够快，就会丢弃旧的消息
    pub = rospy.Publisher('chatter2', my_string, queue_size= 10)
    
    # pub_my = rospy.Publisher('my_msg', my_string, queue_size = 10)
    ##初始化节点，开始跟rosmaster通讯，节点名字在网络中是唯一的，不能包含斜杠'/'
    rospy.init_node('talker2', anonymous=True)

    ##创建Rate 对象，与sleep()函数结合使用，控制话题发布的频率
    rate = rospy.Rate(10) ##10Hz

    count = 0

    while not rospy.is_shutdown():
        talk2_str = my_string()
        
        # talk2_str.header.stamp = rospy.Time(count)
        talk2_str.header.stamp = rospy.Time.now()
        talk2_str.data = "talker2 %s" % talk2_str.header.stamp.to_sec()

        rospy.loginfo(talk2_str)



        pub.publish(talk2_str)

        count += 1
        rate.sleep()

        


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInternalException:
        pass
