# Docker Instruction 

## Ubuntu 22 + ROS2 Humble + XBot2 + Cartesio + Doosan Models

### Build cointaner
- `cd` in this (docker) folder
- `docker compose build`  

### Run Container
- `cd` in this (docker) folder
- `docker compose up -d`

### Enter Container 
- `docker exec -it magician_xbot2 bash`

#### First time run
If this is first time running, you want to clone the doosan model repo:
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
