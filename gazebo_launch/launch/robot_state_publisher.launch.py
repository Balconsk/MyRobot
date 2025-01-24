from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.conditions import IfCondition
from launch.substitutions import Command


def generate_launch_description():

    ld = LaunchDescription()

    this_package = "gz_launch_tutorial"
    xacro_file = "my_bot.urdf.xacro"

    urdf_package_arg = DeclareLaunchArgument(
        name="urdf_package", default_value=this_package
    )

    ld.add_action(urdf_package_arg)

    urdf_package_path_arg = DeclareLaunchArgument(
        name="path_to_urdf", default_value=PathJoinSubstitution(["urdf", xacro_file])
    )

    ld.add_action(urdf_package_path_arg)

    urdf_path = PathJoinSubstitution(
        [
            FindPackageShare(LaunchConfiguration("urdf_package")),
            LaunchConfiguration("path_to_urdf"),
        ]
    )

    robot_description_content = ParameterValue(
        Command(["xacro ", urdf_path]), value_type=str
    )

    ld.add_action(
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[
                {
                    "robot_description": robot_description_content,
                }
            ],
        )
    )

    return ld
