# iit-doosan-ros-pkg
Models for the doosan robot integrated in XBot2 ROS2 version humble

## How to Install 
- Install XBot2 dependecies 
  - `sudo apt install -y ros-humble-srdfdom ros-humble-geometric-shapes`
- Install CartesI/O dependencies
  - `sudo apt install -y ros-humble-moveit-msgs`
- Install XBot2:
  ```
  sudo sh -c 'echo "deb http://xbot.cloud/xbot2-nightly/ubuntu/$(lsb_release -sc) /" > /etc/apt/sources.list.d/xbot-latest.list'
  wget -q -O - http://xbot.cloud/xbot2-nightly/ubuntu/KEY.gpg | sudo apt-key add -
  sudo apt update
  sudo apt install xbot2_desktop_full
  ```
- Install XBot2 GUI
  *TODO*
- Clone this repo, models and meshes are here so no need for the official doosan robot repo:
  ```
  mkdir -p ~/ros_ws/src && cd ~/ros_ws/src
  git clone https://github.com/magician-project/iit-doosan-ros-pkg.git
  ```
- Build it with `colcon build` (do not use `--symlink-install` since for some mysterious reasons the node 
`pub_robot_description` is not found if it is only a link)
  ```
  source /opt/ros/humble/setup.bash
  source /opt/xbot/setup.bash
  cd ~/ros_ws
  colcon build
  ```
- Conveniently source everytime putting these in the bashrc:
  ```
  echo source /opt/ros/$ROS_DISTRO/setup.bash >> ~/.bashrc
  echo source ~/ros_ws/install/setup.bash >> ~/.bashrc
  echo source /opt/xbot/setup.sh >> ~/.bashrc
  ```

### Docker Version
Check [docker folder](docker)

## How to setup
- Select a xbot config file:
  `set_xbot2_config ~/ros_ws/iit-doosan-ros-pkg/doosan_xbot2_config/h2515_xbot.yaml`
  Choose the end-effector by passing the 'gripper' argument to urdf.xacro and srdf.xacro at the top of such config file, such as 
  ```yaml
  urdf: xacro $(ros2 pkg prefix --share doosan_urdf)/urdf/h2515.urdf.xacro gripper:=dewalt
  srdf: xacro $(ros2 pkg prefix --share doosan_srdf)/srdf/h2515.srdf.xacro gripper:=dewalt
  ```


## How to Use
*Be sure to have sourced xbot, ros, and ros_ws workspace, put them the bashrc for convenience*

### RViz only (no dynamic)
1) Terminal 1: `ros2 launch doosan_urdf h2515.launch`
2) Terminal 2: `xbot2-core --hw dummy`

### Gazebo (dynamic simulation)
1) Terminal 1: `ros2 launch doosan_gazebo h2515.launch.py` (*note* pass `gripper` argument according to the xbot config file, like `gripper:=dewalt`)
2) Terminal 2: `xbot2-core --simtime` (*note*: `--hw sim` is the default)
3) Play the simulation (gazebo gui button) - I am looking for a working way to start it automatically

### Optional
#### GUI
1) Terminal 1: `xbot2_gui_server`
2) Terminal 2: `xbot2_gui`

#### CartesI/O ros_node
1) `ros2 launch doosan_cartesio h2515.launch #ci_rviz:=true markers:=true`


