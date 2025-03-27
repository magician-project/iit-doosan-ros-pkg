cmake_minimum_required(VERSION 3.20)
project(doosan_xbot2_config)

find_package(ament_cmake REQUIRED)

install(DIRECTORY hal
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY conf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()