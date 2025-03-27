# Doosan XBot Launch file

This repository contains a set of [launch files](./launch) to simplified the launch of ROS2 application, with the focus on simplifying the transition from simulation to real robot.

The main launch file [`h2515_bringup.launch.py`](./launch/h2515_bringup.launch.py) can be used to bootstrap the environment
``` bash
ros2 launch doosan_bringup h2515_bringup.launch.py
```
By default, this launch file opens the Gazebo Ignition simulation environment and executes all XBot2 scripts.

The behavior of the file can be customized with the following list of launch arguments.



## Launch arguments

- `gripper` (type: string, default value: `dewalt`): gripper mounted at the end-effector of the robot. 
  Possible values are `dewalt` or `none`;
- `setup` (type: string, default value: `iit`): 
  environment in which the robot which shall be used to spawn the robot into. Possible values are `none` or `iit`;
- `simulator` (type: boolean, default value: `true`): 
  if on, the robot is loaded in the Gazebo ignition simulation environment. Otherwise, a connection on the real robot is assumed;
- `rviz` (type: boolean, default value: `true`): 
  if set, RViz2 is started from this script by using the specified `rviz_config` config file;
- `rviz_config` (type: string path, default value: [`rviz/h2515.rviz`](./rviz/h2515.rviz)): 
  RViz2 configuration file used for visualising the environment;
- `xbot` (type: boolean, default value: `true`): 
  if on, the [`xbot2`](https://advrhumanoids.github.io/xbot2/master/index.html) are executed from this script;
