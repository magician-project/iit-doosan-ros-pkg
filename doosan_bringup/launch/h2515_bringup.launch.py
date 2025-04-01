from launch.event_handlers import OnProcessExit, OnExecutionComplete
import xacro
import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    RegisterEventHandler,
    TimerAction,
    ExecuteProcess,
    LogInfo,
    SetEnvironmentVariable,
)
from launch.substitutions import Command, LaunchConfiguration, FindExecutable
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import (
    PythonLaunchDescriptionSource,
    AnyLaunchDescriptionSource,
)
from launch_ros.parameter_descriptions import ParameterValue

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import (
    get_package_prefix,
    get_package_share_path,
)


AVAILABLE_GRIPPERS = [
    "dewalt",
    "none",
]
AVAILABLE_SETUPS = [
    "iit",
    "none",
]


def launch_setup(context, *args, **kwargs):

    nodes_to_start = []

    gripper = LaunchConfiguration("gripper").perform(context)
    setup = LaunchConfiguration("setup").perform(context)
    rviz = LaunchConfiguration("rviz").perform(context)
    rviz_config = LaunchConfiguration("rviz_config").perform(context)
    simulator = LaunchConfiguration("simulator").perform(context)
    with_xbot = LaunchConfiguration("xbot").perform(context)
    component = LaunchConfiguration("component", default="right_back_door").perform(context)
    use_sim_time = (simulator == "true")

    ###
    ### ROBOT DESCRIPTION
    ###
    if simulator == "true":
        xacro_file = os.path.join(
            get_package_share_path("doosan_gazebo"), "urdf", "h2515_gazebo.urdf.xacro"
        )
    else:
        xacro_file = os.path.join(
            get_package_share_path("doosan_urdf"), "urdf", "h2515.urdf.xacro"
        )
    robot_description_content = xacro.process(
        xacro_file, mappings={
            "gripper": gripper,
            "setup": setup,
        }
    )
    robot_description = {"robot_description": robot_description_content}

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description, {
            "use_sim_time": use_sim_time,
        }],
    )
    nodes_to_start += [
        robot_state_publisher_node,
    ]

    ###
    ### SIMULATOR
    ###
    world_file = os.path.join(
        get_package_share_path("doosan_gazebo"), "world", "doosan.world"
        # get_package_share_path("doosan_gazebo"), "world", f"doosan_{component}.world"
    )
    ignition_simulator_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("ros_gz_sim"), "/launch/gz_sim.launch.py"
        ], ),
        launch_arguments={
            "gz_args": f" -r -v 1 {world_file}",
        }.items(),
        condition=IfCondition(simulator)
    )

    ignition_spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-name", "h2515", "-topic", "/robot_description"],
        condition=IfCondition(simulator)
    )


    ignition_spawn_meshes = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            FindPackageShare("magician_localisation"), "/launch/mesh_spawner.launch.py"
        ], ),
        # launch_arguments={
            # "gz_args": f" -r -v 1 {world_file}",
        # }.items(),
        condition=IfCondition(simulator)
    )

    nodes_to_start += [
        ignition_simulator_node,
        ignition_spawn_robot,
        ignition_spawn_meshes,
    ]

    ###
    ### XBOT2
    ###
    xbot_core_arguments = [
        "--config",
        os.path.join(get_package_share_path("doosan_xbot2_config"), "h2515_xbot.yaml"),
    ]
    if simulator == "true":
        xbot_core_arguments += ["--simtime"]

    xbot_core = ExecuteProcess(
        cmd=[FindExecutable(name="xbot2-core"), *xbot_core_arguments],
        output="screen",
        condition=IfCondition(with_xbot),
    )

    cartesio_share = get_package_share_path("doosan_cartesio")
    cartesio_launch_file = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            launch_file_path=os.path.join(cartesio_share, "launch", "h2515.launch"),
        ),
        condition=IfCondition(with_xbot),
    )
    cartesio_delayed = TimerAction(
        period=3.0,
        actions=[cartesio_launch_file],
    )

    if simulator == "true":
        cartesio_delayed_on_spawn = RegisterEventHandler(
            OnProcessExit(
                target_action=xbot_core, on_exit=[
                    cartesio_delayed,
                ]
            )
        )
        nodes_to_start += [
            xbot_core,
            cartesio_delayed,
        ]
    else:
        nodes_to_start += [
            xbot_core,
            cartesio_delayed,
        ]

    ###
    ### RVIZ
    ###
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        condition=IfCondition(rviz),
    )

    nodes_to_start += [
        rviz_node,
    ]
    return nodes_to_start


def generate_launch_description():
    declared_arguments = []

    rviz_config_default = os.path.join(
        get_package_share_path("doosan_bringup"), "rviz", "h2515.rviz"
    )

    ###
    ### LAUNCH ARGUMENTS
    ###
    declared_arguments.append(
        DeclareLaunchArgument(
            "gripper",
            default_value="dewalt",
            description=
            f"Environment setup. Possibilities: {', '.join(AVAILABLE_GRIPPERS)}",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "setup",
            default_value="iit",
            description=
            f"Environment setup. Possibilities: {', '.join(AVAILABLE_SETUPS)}",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "simulator", default_value="true", description="Launch simulation?"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument("rviz", default_value="true", description="Launch RViz?")
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "xbot", default_value="true", description="Launch XBot scripts?"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "rviz_config",
            default_value=rviz_config_default,
            description="Path to RViz configuration file"
        )
    )

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
