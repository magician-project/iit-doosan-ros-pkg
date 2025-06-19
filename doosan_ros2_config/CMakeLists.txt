cmake_minimum_required(VERSION 3.10)
project(doosan_ros2_config)

find_package(ament_cmake REQUIRED)

set(ROS2_DDS_IMPLEMENTATION "cyclonedds" CACHE STRING "Select DDS implementation to be used with ros2" )
set(ROS2_IP "" CACHE STRING "Ip address of the interface to be used for ROS2 communication")

add_subdirectory(dds/${ROS2_DDS_IMPLEMENTATION})

# ament
ament_package()