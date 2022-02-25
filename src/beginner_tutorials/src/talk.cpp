/*
 * @Author: your name
 * @Date: 2022-02-17 22:59:34
 * @LastEditTime: 2022-02-17 23:01:29
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: /src/beginner_tutorials/src/talk.cpp
 */
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "beginner_tutorials/Num.h"


#include <sstream>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "talker");
    
    ros::NodeHandle n;

    ros::Publisher pub = n.advertise<std_msgs::String>("chatter", 1000);
    ros::Publisher pub_my = n.advertise<beginner_tutorials::Num>("my_msg", 1000);
    
    ros::Rate loop_rate(10);

    int count = 0;
    while (ros::ok())
    {
        std_msgs::String msg1;
        beginner_tutorials::Num my_msg;

        std::stringstream ss;
        ss << "hello world " << count;
        msg1.data = ss.str();

        ROS_INFO("%s", msg1.data.c_str());
        

        my_msg.first_name = "paul";
        my_msg.last_name = "george";
        my_msg.num = 64;
        my_msg.age = 29;
        my_msg.score = 13;

        ROS_INFO("%s", my_msg.last_name.c_str());
        pub.publish(msg1);
        pub_my.publish(my_msg);


        ros::spinOnce();

        loop_rate.sleep();

        count++;
    }

    return 0;
}