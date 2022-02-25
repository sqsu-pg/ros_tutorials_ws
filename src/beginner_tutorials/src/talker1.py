#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String

from beginner_tutorials.msg import my_string


def talker():
    ##queue_size 表示队列的大小，如果消息队列处理不够快，就会丢弃旧的消息
    pub = rospy.Publisher('chatter1', my_string, queue_size= 10)
    
    # pub_my = rospy.Publisher('my_msg', my_string, queue_size = 10)
    ##初始化节点，开始跟rosmaster通讯，节点名字在网络中是唯一的，不能包含斜杠'/'
    rospy.init_node('talker1', anonymous=True)

    ##创建Rate 对象，与sleep()函数结合使用，控制话题发布的频率
    rate = rospy.Rate(2) ##10Hz

    count = 0

    while not rospy.is_shutdown():
        talk1_str = my_string()
        
        # talk1_str.header.stamp = rospy.Time(count)
        talk1_str.header.stamp = rospy.Time.now()
        talk1_str.data = "talker1 %s" % talk1_str.header.stamp.to_sec()

        rospy.loginfo(talk1_str)



        pub.publish(talk1_str)

        count += 1
        rate.sleep()

        


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInternalException:
        pass
