cmake_minimum_required(VERSION 3.20)
project(doosan_cartesio)

find_package(ament_cmake REQUIRED)

# mark srdf for installation
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
install(DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME}
)


ament_package()