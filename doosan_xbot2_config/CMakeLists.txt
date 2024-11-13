cmake_minimum_required(VERSION 3.20)
project(doosan_xbot2_config)

find_package(ament_cmake REQUIRED)

install(DIRECTORY hal
  DESTINATION share/${PROJECT_NAME}
)

install(FILES h2515_xbot.yaml 
  DESTINATION share/${PROJECT_NAME}
)

ament_package()