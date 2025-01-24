from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition


def generate_launch_description():

    world_name = "tugbot_warehouse.sdf"
    this_package = "gazebo_launch"
    this_package_share = FindPackageShare(this_package)
    bridge_params = PathJoinSubstitution(
        [this_package_share, "config", "gz_bridge_config.yaml"]
    )

    ld = LaunchDescription()

    # DELCARE LAUNCH ARGUMENT
    # rviz
    ld.add_action(
        DeclareLaunchArgument(
            name="rviz", default_value="true", choices=["true", "false"]
        )
    )
    ld.add_action(
        DeclareLaunchArgument(
            name="rviz_config",
            default_value=PathJoinSubstitution(
                [this_package_share, "config", "rviz_config.rviz"]
            ),
            description="Absolut path to rviz config file",
        )
    )

    # join state publisher
    ld.add_action(
        DeclareLaunchArgument(
            name="jsp",
            default_value="false",
            choices=["false", "true"],
            description="Flag to enabel join state publisher gui",
        )
    )

    # robot state publisher
    ld.add_action(
        DeclareLaunchArgument(
            name="rsp",
            default_value="true",
            choices=["true", "false"],
            description="Flag to enabel robot state publisher",
        )
    )

    ld.add_action(
        DeclareLaunchArgument(
            name="path_to_urdf",
            default_value=PathJoinSubstitution(
                ["urdf", "my_robot_urdf", "my_robot_urdf.xacro"]
            ),
        )
    )

    ld.add_action(
        DeclareLaunchArgument(name="urdf_package", default_value="robot_description")
    )

    # NODE DESCRIPTION
    # gazebo bridgs for img
    gz_bridge_msg = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=["/camera/image_raw"],
        output="screen",
    )

    # gazebo bridgs for msg
    gz_bridge_img = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments={
            "--ros-args": "",
            "-p": "",
            "config_file:=": bridge_params,
        }.items(),
    )

    # RVIZ2
    rviz2 = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["use_sim_time:=true", "-d", LaunchConfiguration("rviz_config")],
        output="screen",
        condition=IfCondition(LaunchConfiguration("rviz")),
    )

    # join state publisher
    jsp = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        condition=IfCondition(LaunchConfiguration("jsp")),
    )

    # robot state publisher
    rsp = IncludeLaunchDescription(
        PathJoinSubstitution(
            [this_package_share, "launch", "robot_state_publisher.launch.py"]
        ),
        launch_arguments={
            "urdf_package": LaunchConfiguration("urdf_package"),
            "path_to_urdf": LaunchConfiguration("path_to_urdf"),
            "use_sim_time": "true",
        }.items(),
        condition=IfCondition(LaunchConfiguration("rsp")),
    )

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

    # gazebo spawn robots
    gz_spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic","robot_description",
            "-name","my_bot",
            "-x","13.38",
            "-y","-10.00",
            "-z","0.5",
        ],
        output="screen",
    )

    # add pointcloud to laserscan
    ponitcloud_to_laserscan = Node(
        package="pointcloud_to_laserscan",
        executable="pointcloud_to_laserscan_node",
        remappings=[("cloud_in", "points")],
        parameters=[
            {
                # 'target_frame': 'base_link',
                # 'transform_tolerance': 0.01,
                "min_height": 0.0,
                "max_height": 200.0,
                "angle_min": -0.5,  # -M_PI/2
                "angle_max": 0.5,  # M_PI/2
                "angle_increment": 0.0087,  # M_PI/360.0
                "scan_time": 1.0,
                "range_min": 0.45,
                "range_max": 10.0,
                "use_inf": True,
                "inf_epsilon": 1.0,
                "use_sim_time": True,
            }
        ],
        name="pointcloud_to_laserscan",
    )

    ld.add_action(rviz2)
    ld.add_action(jsp)
    ld.add_action(rsp)
    ld.add_action(gz_sim)
    ld.add_action(gz_spawn_robot)
    ld.add_action(gz_bridge_msg)
    ld.add_action(gz_bridge_img)
    ld.add_action(ponitcloud_to_laserscan)
    return ld
