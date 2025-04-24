from launch import LaunchDescription
from launch.substitutions import  PathJoinSubstitution,  PythonExpression
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():

    world_name = "world.sdf"
    this_package = "gazebo_launch"
    this_package_share = FindPackageShare(this_package)

    ld = LaunchDescription()


    # gazebo launch
    gz_sim = IncludeLaunchDescription(
        PathJoinSubstitution(
            [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
        ),
        launch_arguments={
            "gz_args": PathJoinSubstitution([this_package_share, "worlds", world_name]),
            "on_exit_shutdown": "true",
        }.items(),
    )

    env_var = AppendEnvironmentVariable("GZ_SIM_RESOURCE_PATH",PathJoinSubstitution([this_package_share, "worlds"]))

    ld.add_action(gz_sim)
    ld.add_action(env_var)
    return ld
