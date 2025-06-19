if(ROS2_IP STREQUAL "")
    message(WARNING "ROS2_IP variable is empty. Will default to localhost.")
    set(ROS2_IP "127.0.0.1")
endif()

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cyclonedds-config.xml.in 
    ${CMAKE_CURRENT_SOURCE_DIR}/cyclonedds-config.xml
    @ONLY 
)

install(
    FILES 10-ros2-config.conf
    DESTINATION /etc/sysctl.d 
    COMPONENT sysctl_rules
    EXCLUDE_FROM_ALL
    )
