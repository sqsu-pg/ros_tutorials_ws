# 1.功能

在实验室服务器上运行的分支

订阅双目图像，之后利用python3版本的cv_bridge，将左目图像使用mask r cnn 进行掩码提取处理，使用raft进行光流提取，并发布出来



# 2.运行步骤

## 2.1 talker

这个是模仿双目相机，发布双目kitti 图像

```bash 
set_ros_pythonpath
#.bashrc 中 alias set_ros_pythonpath='export PYTHONPATH="/usr/lib/python2.7/dist-packages"'
##因为默认使用的python2.7位 /usr/local/bin/python, 需要使用/usr/bin/python


source /opt/ros/melodic/setup.bash
##更新ros 工作空间

cd  ~/ros_tutorials_ws/src/beginner_tutorials/src
python2 talk_left_right_pic.py 
```

## 2.2 listener_stereo_and_pub_maskflo

订阅双目图像，计算mask,flo 并发布出去

```bash 
conda activate grad_deep_learn

source ~/catkin_workspace/devel/setup.bash 
#这个是python3版本的cv_bridge所在的ros工作空间，使得python3可以找到cv_bridge

source ~/ros_tutorials_ws/devel/setup.bash
#更新当前工作空间，因为需要使用到当前工作空间自定义的msgs

python listener_stereo_and_pub_maskflo.py
#运行ros 节点
```



## 2.3 split_topic for vis

```bash
source ~/catkin_workspace/devel/setup.bash 
#这个是python3版本的cv_bridge所在的ros工作空间，使得python3可以找到cv_bridge

source ~/ros_tutorials_ws/devel/setup.bash
#更新当前工作空间，因为需要使用到当前工作空间自定义的msgs

rosrun beginner_tutorials lis_stereo_mask_flo_split
#运行ros 节点
```

