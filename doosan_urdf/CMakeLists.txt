cmake_minimum_required(VERSION 3.20)
project(doosan_urdf)

find_package(ament_cmake REQUIRED)

install(DIRECTORY launch
 DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY meshes
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY rviz
  DESTINATION share/${PROJECT_NAME}
)

# ament
ament_package()
