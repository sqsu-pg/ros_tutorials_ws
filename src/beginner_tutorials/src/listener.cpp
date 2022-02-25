#include "ros/ros.h"
#include "std_msgs/String.h"
#include "beginner_tutorials/Num.h"

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
    ROS_INFO("I heard: [%s]", msg->data.c_str());
}

void mymsgCallback(const beginner_tutorials::Num::ConstPtr& msg)
{
    ROS_INFO("I heard: [%s]", msg->last_name.c_str());
}

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "listener");

    ros::NodeHandle n;

    ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);
    ros::Subscriber sub_my = n.subscribe("my_msg", 1000, mymsgCallback);
    
    ros::spin();

    return 0;
}

