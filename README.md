# iit-doosan-ros-pkg
Models for the doosan robot integrated in XBot2 ROS2 version humble

## How to Install 
- Install XBot2 dependecies 
  - `sudo apt install -y ros-humble-srdfdom ros-humble-geometric-shapes`
- Install CartesI/O dependencies
  - `sudo apt install -y ros-humble-moveit-msgs`
- Install other necessary dependencies:
  - `sudo apt install -y ros-humble-xacro`
- Download and install XBot2 debs:
  ```
  cd ~ && mkdir deb && cd deb
  wget -r -np -nH --cut-dirs=1 -R "index.html*" http://xbot.cloud/magician-deb/upload
  sudo dpkg -i ./upload/*.deb
  ```
- Clone this repo, models and meshes are here so no need for the official doosan robot repo:
  ```
  mkdir -p ~/ros_ws/src && cd ~/ros_ws/src
  git clone https://github.com/magician-project/iit-doosan-ros-pkg.git
  ```
- Build it with `colcon build` (do not use `--symlink-install` since for some mysterious reasons the node 
`pub_robot_description` is not found if it is only a link)
  ```
  source /opt/ros/humble/setup.bash
  source /opt/xbot/setup.sh
  cd ~/ros_ws
  colcon build
  ```
- Conveniently source everytime putting these in the bashrc:
  ```
  echo source /opt/ros/$ROS_DISTRO/setup.bash >> ~/.bashrc
  echo source ~/ros_ws/install/setup.bash >> ~/.bashrc
  echo source /opt/xbot/setup.sh >> ~/.bashrc
  source ~/.bashrc
  ```

### Docker Version
Check [docker folder](docker)

## How to setup
- Select a xbot config file:
  `set_xbot2_config ~/ros_ws/src/iit-doosan-ros-pkg/doosan_xbot2_config/conf/h2515_xbot.yaml`  
  Choose the end-effector by passing the 'gripper' argument to urdf.xacro and srdf.xacro at the top of such config file, such as 
  ```yaml
  urdf: xacro $(ros2 pkg prefix --share doosan_urdf)/urdf/h2515.urdf.xacro gripper:=dewalt
  srdf: xacro $(ros2 pkg prefix --share doosan_srdf)/srdf/h2515.srdf.xacro gripper:=dewalt
  ```


## How to Use
*Be sure to have sourced ros, ros_ws, and xbot (in this order) before running in each terminal. You can put them the bashrc for convenience*

### RViz only (no dynamic)
1) Terminal 1: `ros2 launch doosan_urdf h2515.launch`
2) Terminal 2: `xbot2-core --hw dummy`

### Gazebo (dynamic simulation)
1) Terminal 1: `ros2 launch doosan_gazebo h2515.launch.py` (*note* pass `gripper` argument according to the xbot config file, like `gripper:=dewalt`)
2) Terminal 2: `xbot2-core --simtime` (*note*: `--hw sim` is the default)
3) Play the simulation (gazebo gui button) - I am looking for a working way to start it automatically

### Real Robot
*pilot + embedded, iit setup: lenovo+zotac*
~~~
magician@ThinkStation22:~$ alias ssh_doosan
alias ssh_doosan='ssh -X zotac22@192.168.137.54'
~~~
~~~
zotac22@zotac22 ~ $ get_xbot2_config 
/home/zotac22/forest_ws/src/doosan_xbot2/doosan_xbot2_hal_config/doosan_xbot2_config.yaml
~~~
#### Embedded
1) Be sure to put right end-effector from the tablet
2) ~xbot2-core --hw doosan~ Close with with ctrl+c **then** ctrl+4 to save logs correctly

#### Pilot
- `ros2 launch doosan_urdf h2515.launch`
- if mesh necessary (after registration) `ros2 launch magician_localisation mesh_spawner.launch.py`
- home the robot
- start `cartesio_imp`, from xbot gui or directly with service. **Take care** robot may move. **Do not** send commands directly to xbot with /xbotcore/command topic or from GUI sliders, now you have to communicate only to upper layer: cartesio


### Optional
#### GUI
1) Terminal 1: `xbot2_gui_server`
2) Terminal 2: `xbot2_gui`

#### CartesI/O ros_node
1) `ros2 launch doosan_cartesio h2515.launch #ci_rviz:=true markers:=true`


## Examples
You can find some example code here https://github.com/magician-project/doosan_examples and some more doc about CartesI/O here (ROS1-based) https://advrhumanoids.github.io/CartesianInterface/

