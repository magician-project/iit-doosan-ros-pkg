cmake_minimum_required(VERSION 3.20)
project(doosan_urdf)

find_package(ament_cmake REQUIRED)

# mark urdf, meshes and launch files for installation
#install(DIRECTORY launch
#  DESTINATION share/${PROJECT_NAME}/launch
#)

install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}/urdf
)

# ament
ament_package()
