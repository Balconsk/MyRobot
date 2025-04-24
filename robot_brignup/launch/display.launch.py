from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration,PythonExpression, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import AppendEnvironmentVariable, DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

import os
import xacro

def generate_launch_description():

    # get package share directory
    robot_brignup = get_package_share_directory("robot_brignup")

    # get path to config rviz
    rviz_config_path = os.path.join(robot_brignup, "config/rviz.rviz")

    

    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["use_sim_time:=true", "-d", PathJoinSubstitution(
                [robot_brignup, "config", "rviz.rviz"]
            )],
        output="screen",
    )

    return LaunchDescription(
        [
            rviz2,
        ]
    )