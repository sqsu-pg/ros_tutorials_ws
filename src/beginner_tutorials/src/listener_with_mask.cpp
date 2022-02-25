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

#include <beginner_tutorials/Img_vec.h>

using namespace std;

void LoadMask(const string &strFilenamesMask, cv::Mat &imMask)
{
    ifstream file_mask;
    file_mask.open(strFilenamesMask.c_str());

    //doing Main loop
    int count = 0;
    while(!file_mask.eof())
    {
        string s;
        getline(file_mask, s);
        if (!s.empty())
        {
            stringstream ss;
            ss << s;
            int tmp;
            for (int i = 0; i < imMask.cols; ++i)
            {
                ss >> tmp;
                if (tmp != 0)
                {
                    imMask.at<int>(count, i) = tmp;
                }
                else 
                {
                    imMask.at<int>(count, i) = 0;
                }
            }
            count++;
        }
    }

    return ;
}

void picWithMaskCallback(const beginner_tutorials::Img_vecConstPtr &img_with_mask_msg)
{
    ROS_INFO("I heard pic_with_mask");

    cv::Mat image_pic, image_mask;
    
    cv_bridge::CvImageConstPtr cv_ptr;

    cv_ptr = cv_bridge::toCvCopy(img_with_mask_msg->image_left);
    cv_ptr->image.copyTo(image_pic);



    cv_bridge::CvImageConstPtr cv_ptr_mask;
    cv_ptr_mask = cv_bridge::toCvCopy(img_with_mask_msg->image_mask);
    cv_ptr_mask->image.copyTo(image_mask);

    std::cout << "image_pic : " << std::endl;
    std::cout << "dtype : " << image_pic.type() << std::endl;
    std::cout << "cols : " << image_pic.cols << std::endl;
    std::cout << "rows : " << image_pic.rows << std::endl;
    std::cout << "channels : " << image_pic.channels() << std::endl;

    
    
    std::cout << "image_mask : " << std::endl;
    std::cout << "dtype : " << image_mask.type() << std::endl;
    std::cout << "cols : " << image_mask.cols << std::endl;
    std::cout << "rows : " << image_mask.rows << std::endl;
    std::cout << "channels : " << image_mask.channels() << std::endl;

    std::cout << "check the image data : " << std::endl;
    std::string image_path = img_with_mask_msg->image_path;
    std::string image_mask_path = img_with_mask_msg->image_mask_path;

    // cv::Mat resource_image = cv::imread(image_path, cv::IMREAD_UNCHANGED);
    cv::Mat resource_image = cv::imread(image_path, 1);

    cv::Mat absDiff = cv::abs(image_pic - resource_image);
    std::cout << "dtype : " << absDiff.type() << std::endl;
    std::cout << "cols : " << absDiff.cols << std::endl;
    std::cout << "rows : " << absDiff.rows << std::endl;
    std::cout << "channels : " << absDiff.channels() << std::endl;

    cv::Scalar ss = cv::sum(absDiff);
    std::cout << "sum of abs diff is : " << ss[0] << std::endl;

    cv::Mat resource_image_mask(resource_image.rows, resource_image.cols, CV_32SC1);
    LoadMask(image_mask_path, resource_image_mask);
    std::cout << "read mask txt : " << std::endl;
    std::cout << "dtype : " << resource_image_mask.type() << std::endl;
    std::cout << "cols : " << resource_image_mask.cols << std::endl;
    std::cout << "rows : " << resource_image_mask.rows << std::endl;
    std::cout << "channels : " << resource_image_mask.channels() << std::endl;

    cv::Mat target_mask;
    image_mask.convertTo(target_mask, CV_32SC1);
    std::cout << "dtype : " << target_mask.type() << std::endl;
    std::cout << "cols : " << target_mask.cols << std::endl;
    std::cout << "rows : " << target_mask.rows << std::endl;
    std::cout << "channels : " << target_mask.channels() << std::endl;

    cv::Mat absDiff2  = cv::abs(resource_image_mask - target_mask);
    cv::Scalar ss2 = cv::sum(absDiff2);
    std::cout << "sum of abs mask diff is : " << ss2[0] << std::endl;

    // cv::imshow("lis_image_pic", image_pic);
    // cv::waitKey(10);
    // cv::imshow("lis_image_mask", image_mask);
    // cv::waitKey(10);


}



int main(int argc, char *argv[])
{
    ros::init(argc, argv, "listener_with_mask");
    
    ros::NodeHandle nh;

    // cv::namedWindow("lis_pic");

    // cv::Mat img_pic;

    ros::Subscriber sub = nh.subscribe("pic_with_mask", 10, picWithMaskCallback);
    // ros::Subscriber sub = nh.subscribe<beginner_tutorials::Img_vec>("pic_with_mask", 10, boost::bind(&picWithMaskCallback, _1, img_pic));

    
    
    // ros::spin();

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
    


    return 0;
}