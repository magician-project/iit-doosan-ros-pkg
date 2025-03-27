cmake_minimum_required(VERSION 3.20)
project(doosan_bringup)

find_package(ament_cmake REQUIRED)

install(
    DIRECTORY launch
    DESTINATION share/${PROJECT_NAME}
)

install(
    DIRECTORY rviz
    DESTINATION share/${PROJECT_NAME}
)

# ament
ament_package()
