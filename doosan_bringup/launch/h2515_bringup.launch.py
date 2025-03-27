from launch.event_handlers.on_process_exit import OnProcessExit
import xacro
import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
    RegisterEventHandler,
)
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
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

    gripper = LaunchConfiguration("gripper").perform(context)
    setup = LaunchConfiguration("setup").perform(context)
    rviz = LaunchConfiguration("rviz").perform(context)
    rviz_config = LaunchConfiguration("rviz_config").perform(context)
    simulator = LaunchConfiguration("simulator").perform(context)

    use_sim_time = (simulator == "true")
    is_simulation = IfCondition(simulator)
    is_real = UnlessCondition(simulator)

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

    print("RViz config path:", rviz_config)
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        arguments=["-d", rviz_config],
        condition=IfCondition(rviz),
    )

    nodes_to_start = [
        robot_state_publisher_node,
        rviz_node,
    ]
    return nodes_to_start


def generate_launch_description():
    declared_arguments = []

    # --- Setup environment variables
    # MDL_ENV_VAR = "IGN_GAZEBO_RESOURCE_PATH"
    # if MDL_ENV_VAR in os.environ:
    #     os.environ[MDL_ENV_VAR] += ":" + os.path.join(
    #         get_package_prefix("z1_description"), "share"
    #     )
    # else:
    #     os.environ[MDL_ENV_VAR] = os.path.join(
    #         get_package_prefix("z1_description"), "share"
    #     )

    # LIB_ENV_VAR = "IGN_GAZEBO_SYSTEM_PLUGIN_PATH"
    # if LIB_ENV_VAR in os.environ:
    #     os.environ[LIB_ENV_VAR] += ":/opt/ros/humble/lib"
    # else:
    #     os.environ[LIB_ENV_VAR] = "/opt/ros/humble/lib"

    rviz_config_default = os.path.join(
        get_package_share_path("doosan_bringup"), "rviz", "h2515.rviz"
    )

    # --- Launch arguments
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
            "rviz_config",
            default_value=rviz_config_default,
            description="Path to RViz configuration file"
        )
    )

    return LaunchDescription(
        declared_arguments + [OpaqueFunction(function=launch_setup)]
    )
