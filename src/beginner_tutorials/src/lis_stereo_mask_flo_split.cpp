#include <ros/ros.h>
#include <cv_bridge/cv_bridge.h>
#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>
#include <string>
#include <sstream>

#include <opencv2/core/core.hpp>
#include <opencv2/opencv.hpp>
#include <boost/bind.hpp>

#include <beginner_tutorials/StereoImageMaskFlo.h>
#include <sensor_msgs/Image.h>

using namespace std;

class SplitTopic
{
    public:
        SplitTopic() 
        {
            // sub = nh.subscribe("AllStereoMsg", 5, SplitCallBack);

            LeftImagePub = nh.advertise<sensor_msgs::Image>("left_image", 5);
            RightImagePub = nh.advertise<sensor_msgs::Image>("right_image", 5);
            MaskImagePub = nh.advertise<sensor_msgs::Image>("mask_image", 5);
            FloImagePub = nh.advertise<sensor_msgs::Image>("flo_image", 5);
            FloVisImagePub = nh.advertise<sensor_msgs::Image>("flo_vis_image", 5);
            FloVis8UC3ImagePub = nh.advertise<sensor_msgs::Image>("flo_vis_image_8UC3", 5);

            mColor_vec.resize(10, std::vector<int>());
            mColor_vec[0].push_back(255);
            mColor_vec[0].push_back(0);
            mColor_vec[0].push_back(0);
            
            mColor_vec[1].push_back(0);
            mColor_vec[1].push_back(255);
            mColor_vec[1].push_back(0);

            mColor_vec[2].push_back(255);
            mColor_vec[2].push_back(255);
            mColor_vec[2].push_back(0);

            mColor_vec[3].push_back(0);
            mColor_vec[3].push_back(0);
            mColor_vec[3].push_back(255);

            mColor_vec[4].push_back(255);
            mColor_vec[4].push_back(0);
            mColor_vec[4].push_back(255);

            mColor_vec[5].push_back(0);
            mColor_vec[5].push_back(255);
            mColor_vec[5].push_back(255);

            mColor_vec[6].push_back(153);
            mColor_vec[6].push_back(50);
            mColor_vec[6].push_back(204);

            mColor_vec[7].push_back(255);
            mColor_vec[7].push_back(185);
            mColor_vec[7].push_back(15);

            mColor_vec[8].push_back(0);
            mColor_vec[8].push_back(139);
            mColor_vec[8].push_back(69);

            mColor_vec[9].push_back(175);
            mColor_vec[9].push_back(238);
            mColor_vec[9].push_back(238);



            // cv::namedWindow("Flo_Vis");
        }

        void SplitCallBack(const beginner_tutorials::StereoImageMaskFloConstPtr &Msg_Ptr)
        {
            ROS_INFO("I heard AllStereoMsg");

            cv::Mat Left_Img, Right_Img, Mask_Img, Flo, Flo_Vis, Flo_Vis_8UC3;

            cv_bridge::CvImageConstPtr cv_ptr_left;
            cv_ptr_left = cv_bridge::toCvCopy(Msg_Ptr->ImageLeft);
            cv_ptr_left->image.copyTo(Left_Img);
            LeftImagePub.publish(cv_ptr_left->toImageMsg());

            cv_bridge::CvImageConstPtr cv_ptr_right;
            cv_ptr_right = cv_bridge::toCvCopy(Msg_Ptr->ImageRight);
            cv_ptr_right->image.copyTo(Right_Img);
            RightImagePub.publish(cv_ptr_right->toImageMsg());

            cv_bridge::CvImageConstPtr cv_ptr_Mask;
            cv_ptr_Mask = cv_bridge::toCvCopy(Msg_Ptr->ImageMask);
            cv_ptr_Mask->image.copyTo(Mask_Img);
            // cv::Mat Mask_Img_U8 =  cv::Mat::zeros(Mask_Img.rows, Mask_Img.cols, CV_8UC3);
            cv::Mat Mask_Img_8UC3 = Left_Img;
            for (int i = 0; i < Mask_Img.rows; i++)
            {
                for (int j = 0; j < Mask_Img.cols; j++)
                {
                    if (Mask_Img.at<int>(i, j) == 0)
                    {
                        continue;
                    }
                    else
                    {
                        int index = Mask_Img.at<int>(i, j) % 9;
                        Mask_Img_8UC3.at<cv::Vec3b>(i, j)[0] = mColor_vec[index][0];
                        Mask_Img_8UC3.at<cv::Vec3b>(i, j)[1] = mColor_vec[index][1];
                        Mask_Img_8UC3.at<cv::Vec3b>(i, j)[2] = mColor_vec[index][2];
                    }
                }
            }
            sensor_msgs::ImagePtr msg_Mask_8UC3 = cv_bridge::CvImage(std_msgs::Header(), "bgr8", Mask_Img_8UC3).toImageMsg();
        
            // MaskImagePub.publish(cv_ptr_Mask->toImageMsg());
            MaskImagePub.publish(msg_Mask_8UC3);

            cv_bridge::CvImageConstPtr cv_ptr_Flo;
            cv_ptr_Flo = cv_bridge::toCvCopy(Msg_Ptr->ImageFlo);
            cv_ptr_Flo->image.copyTo(Flo);
            FloImagePub.publish(cv_ptr_Flo->toImageMsg());

            cv_bridge::CvImageConstPtr cv_ptr_Flo_Vis;
            cv_ptr_Flo_Vis = cv_bridge::toCvCopy(Msg_Ptr->ImageFloVis);
            cv_ptr_Flo_Vis->image.copyTo(Flo_Vis);
            FloVisImagePub.publish(cv_ptr_Flo_Vis->toImageMsg());

            Flo_Vis.convertTo(Flo_Vis_8UC3, CV_8UC3);

            sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", Flo_Vis_8UC3).toImageMsg();
            // 发布图像
            FloVis8UC3ImagePub.publish(msg);
            // cv::imshow("Flo_Vis", Flo_Vis);
        }

        void listener()
        {
            ros::Subscriber sub = nh.subscribe("AllStereoMsg", 5, &SplitTopic::SplitCallBack, this);

            while (ros::ok())
            {
                /* code for loop body */
                ros::spinOnce();
                // std::cout << "main pic : " << std::endl;
                // std::cout << "dtype : " << img_pic.type() << std::endl;
                // std::cout << "cols : " << img_pic.cols << std::endl;
                // std::cout << "rows : " << img_pic.rows << std::endl;
                // std::cout << "channels : " << img_pic.channels() << std::endl;

                // cv::imshow("lis_pic", img_pic);
                // cv::waitKey(10);  
            }
        }

        ~SplitTopic()
        {
            // cv::destroyAllWindows();
        }




    private:
        ros::NodeHandle nh;
        ros::Publisher LeftImagePub;
        ros::Publisher RightImagePub;
        ros::Publisher MaskImagePub;
        ros::Publisher FloImagePub;
        ros::Publisher FloVisImagePub;
        ros::Publisher FloVis8UC3ImagePub;

        std::vector<std::vector<int>> mColor_vec;

        

};


int main(int argc, char *argv[])
{
    ros::init(argc, argv, "listener_all_msgs");
    
    SplitTopic Lis1 = SplitTopic();

    Lis1.listener();
    
    return 0;
}