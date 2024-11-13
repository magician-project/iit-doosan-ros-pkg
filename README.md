# iit-doosan-ros-pkg
Models for the doosan robot integrated in xbot2 ROS2 version humble

### How to Install / Setup
- Install xbot dependecies (`ros-humble-srdfdom`, `ros-humble-geometric-shapes`)
- Install xbot from binaries, TODO
- Clone this repo, models and meshes are here so no need for the official doosan robot repo

- Select a xbot config file, `set_xbot2_config src/iit-doosan-ros-pkg/doosan_xbot2_config/h2515_xbot.yaml`

### Docker Version
A docker is available, TODO

### How to Use
#### RViz only (no dynamic)
1) Terminal 1: `ros2 launch doosan_urdf h2515.launch`
2) Terminal 2: `xbot2-core --hw dummy`

#### Gazebo (dynamic simulation)
1) Terminal 1: `ros2 launch doosan_gazebo h2515.launch.py`
2) Terminal 2: `xbot2-core --simtime` (*note*: `--hw sim` is the default)




