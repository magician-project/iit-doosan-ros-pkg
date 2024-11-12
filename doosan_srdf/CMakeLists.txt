cmake_minimum_required(VERSION 3.20)
project(doosan_srdf)

find_package(ament_cmake REQUIRED)

# mark srdf for installation
install(DIRECTORY srdf
  DESTINATION share/${PROJECT_NAME}/srdf
)

ament_package()