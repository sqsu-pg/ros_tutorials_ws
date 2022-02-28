import rospy 
from sensor_msgs.msg import Image
from beginner_tutorials.msg import StereoImageMaskFlo 
import message_filters

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

sys.path.append('/home/liubo/Mask_RCNN/samples')
from Mask_class import Mask

sys.path.append('/home/liubo/optional_flow/RAFT')
from RAFT_Class import RAFT_FLO


# sys.path.append('/opt/ros/melodic/lib/python2.7/dist-packages')
# sys.path.remove('/home/liubo/anaconda3/envs/grad_deep_learn/lib/python3.6/site-packages')

# bridge = CvBridge()


# def callback(data):
#     rospy.loginfo("I heard")

#     Cv_Image_Left = bridge.imgmsg_to_cv2(data)

#     print (type(Cv_Image_Left))
#     print (Cv_Image_Left.shape)
#     print (Cv_Image_Left.dtype)





class ListenAndProcessImage:
    def __init__(self):
        self.bridge = CvBridge()
        self.MaskNet = Mask()

        self.FloNet = RAFT_FLO()

        self.pub_stereo_msg = rospy.Publisher('/AllStereoMsg', StereoImageMaskFlo, queue_size=5)

        self.Pic_Id = 0
        
    
    def callback(self, left_data, right_data):
        Image_cv_left = self.bridge.imgmsg_to_cv2(left_data)
        print (Image_cv_left.shape)
        print (type(Image_cv_left))
        print (Image_cv_left.dtype)
        # cv2.imshow("LeftImage", Image_cv_left)
        # cv2.waitKey(3)

        ##successfully using Mask R CNN
        rospy.loginfo("using mask r cnn : ")
        Image_cv_left_Mask = self.MaskNet.GetAndReturnMask(Image_cv_left.copy())
        rospy.loginfo("mask r cnn res dtype : ")
        print (Image_cv_left_Mask.dtype) #np.int32

        ##USING RAFT FLO
        flo_cv_msg = Image()
        flo_cv_vis_msg = Image()

        if self.Pic_Id == 0:
            self.IMG_CUR = Image_cv_left

            first_flo = np.zeros((Image_cv_left.shape[0], Image_cv_left.shape[1], 2))
            rospy.loginfo("flo.shape: ")
            print (first_flo.shape)

            first_flo_vis = np.zeros(Image_cv_left.shape)


            flo_cv_msg = self.bridge.cv2_to_imgmsg(first_flo)
            flo_cv_vis_msg = self.bridge.cv2_to_imgmsg(first_flo_vis)
            
            print ("id is : ", self.Pic_Id)
            self.Pic_Id += 1
        
        else:
            self.IMG_PER = self.IMG_CUR
            self.IMG_CUR = Image_cv_left

            
            flo_vec = self.FloNet.GetFloAndReturnMatWithVis(self.IMG_PER, self.IMG_CUR)
            Image_cv_flo = flo_vec[0]
            rospy.loginfo("flo.shape: ")
            print (Image_cv_flo.shape)

            Image_cv_flo_vis = flo_vec[1]

            flo_cv_msg = self.bridge.cv2_to_imgmsg(Image_cv_flo)
            flo_cv_vis_msg = self.bridge.cv2_to_imgmsg(Image_cv_flo_vis)



            print ("Id is ", self.Pic_Id)
            self.Pic_Id += 1


        MsgToStereo = StereoImageMaskFlo()
        MsgToStereo.header.stamp.secs = left_data.header.stamp.secs
        MsgToStereo.ImageLeft = left_data
        MsgToStereo.ImageRight = right_data
        MsgToStereo.ImageMask = self.bridge.cv2_to_imgmsg(Image_cv_left_Mask)
        MsgToStereo.ImageFlo = flo_cv_msg
        MsgToStereo.ImageFloVis = flo_cv_vis_msg

        rospy.loginfo("publish")
        self.pub_stereo_msg.publish(MsgToStereo)


    
    def listener(self):
        left_sub = message_filters.Subscriber('left_cam', Image)
        right_sub = message_filters.Subscriber('right_cam', Image)

        ts = message_filters.ApproximateTimeSynchronizer([left_sub, right_sub], 1, 0.1)

        ts.registerCallback(self.callback)

if __name__ == '__main__':
    rospy.init_node("process_image_stereo", anonymous=True)

    Process1 = ListenAndProcessImage()
    Process1.listener()
    
    cv2.destroyAllWindows()

    rospy.spin()