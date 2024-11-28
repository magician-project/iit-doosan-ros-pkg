# iit-doosan-ros-pkg
Models for the doosan robot integrated in xbot2 ROS2 version humble

### How to Install / Setup
- Install xbot dependecies 
  - `sudo apt install -y ros-humble-srdfdom ros-humble-geometric-shapes`
- Install CartesI/O dependencies
  - `sudo apt install -y ros-humble-moveit-msgs`
- Install xbot from binaries, TODO
- Clone this repo, models and meshes are here so no need for the official doosan robot repo
- Build it with `colcon build` (do not use `--symlink-install` since for some misterious reasons the node 
`pub_robot_description` is not found if it is only a link)

- Select a xbot config file, `set_xbot2_config src/iit-doosan-ros-pkg/doosan_xbot2_config/h2515_xbot.yaml`

### Docker Version
Check [docker folder](docker)

### How to Use
#### RViz only (no dynamic)
1) Terminal 1: `ros2 launch doosan_urdf h2515.launch`
2) Terminal 2: `xbot2-core --hw dummy`

#### Gazebo (dynamic simulation)
1) Terminal 1: `ros2 launch doosan_gazebo h2515.launch.py`
2) Terminal 2: `xbot2-core --simtime` (*note*: `--hw sim` is the default)
3) Play the simulation (gazebo gui button) - I am looking for a working way to start it automatically

### Optional
#### GUI
1) Terminal 1: `xbot2_gui_server`
2) Terminal 2: `xbot2_gui`

#### CartesI/O ros_node
1) ros2 launch doosan_cartesio h2515.launch #ci_rviz:=true markers:=true


