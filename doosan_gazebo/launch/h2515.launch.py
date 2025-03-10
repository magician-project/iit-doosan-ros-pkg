import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    SetLaunchConfiguration,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # External args
    color_arg = DeclareLaunchArgument("color", default_value="white")
    gripper_arg = DeclareLaunchArgument("gripper", default_value="")
    x_arg = DeclareLaunchArgument("x", default_value="0")    
    y_arg = DeclareLaunchArgument("y", default_value="0")
    z_arg = DeclareLaunchArgument("z", default_value="0")
    R_arg = DeclareLaunchArgument("R", default_value="0")
    P_arg = DeclareLaunchArgument("P", default_value="0")
    Y_arg = DeclareLaunchArgument("Y", default_value="0")
    rviz_arg = DeclareLaunchArgument("rviz", default_value="true")

    # Setup project paths
    pkg_project = get_package_share_directory('doosan_gazebo')
    pkg_doosan_urdf = get_package_share_directory('doosan_urdf')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Opaque function to use the launch argument inside here
    def create_robot_description(context):
        robot_xacro = os.path.join(pkg_project, "urdf/", "h2515_gazebo.urdf.xacro")
        assert os.path.exists(robot_xacro), "The h2515_gazebo.urdf.xacro doesnt exist in " + str(robot_xacro)
        robot_description_config = xacro.process_file(
            robot_xacro,
            mappings={
                "color": context.launch_configurations["color"],
                "gripper": context.launch_configurations["gripper"],
            },
        )
        robot_desc = robot_description_config.toxml()

        return [SetLaunchConfiguration("robot_desc", robot_desc)]

    create_robot_description_arg = OpaqueFunction(
        function=create_robot_description
    )

    pub_robot_description = Node (
        package="doosan_gazebo",
        executable="pub_robot_description",
        name="pub_robot_description",
        output="screen",
        parameters=[
            {"urdf_string": LaunchConfiguration("robot_desc")},
            {"topic_name": "robot_description"},
        ],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            os.path.join(pkg_doosan_urdf, "rviz", "h2515_rviz.rviz"),
        ],
        condition=IfCondition(LaunchConfiguration("rviz")),
        parameters=[
            {"use_sim_time": True},
        ],
    )


    # Simulator launch file
    world_file = pkg_project + '/world/doosan.world'
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")),
        launch_arguments={
            'gz_args': world_file
        }.items()
    )

    # Spawn robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        name='h2515_urdf_spawner',
        arguments=[
            "-name", "h2515",
            "-entity", "model",
            "-x", LaunchConfiguration('x'),
            "-y", LaunchConfiguration('y'),
            "-z", LaunchConfiguration('z'),
            "-R", LaunchConfiguration('R'),
            "-P", LaunchConfiguration('P'),
            "-Y", LaunchConfiguration('Y'),
            "-topic", "/robot_description",
        ],
        output="screen",
    )

    return LaunchDescription([
        rviz_arg,
        color_arg,
        gripper_arg,
        x_arg,
        y_arg,
        z_arg,
        R_arg,
        P_arg,
        Y_arg,
        create_robot_description_arg,
        gz_sim,
        pub_robot_description,
        spawn_robot,
        rviz,
    ])