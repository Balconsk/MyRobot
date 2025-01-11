from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition
def generate_launch_description():
    
    ld = LaunchDescription()

    
    # Init varibalse
    this_package = "gazebo_launch"
    path_to_xacro = PathJoinSubstitution(["urdf","my_robot_urdf", "my_robot_urdf.xacro"])
    xacro_package = "robot_description"
    

    this_package_share = FindPackageShare(this_package)
    default_rviz_config_path = PathJoinSubstitution([this_package_share, 'config', 'rviz_config.rviz'])
    bridge_params = PathJoinSubstitution([this_package_share, 'config', 'gz_bridge_config.yaml'])
    
    # rviz 
    ld.add_action(DeclareLaunchArgument (name = "rviz", default_value="true", choices=['true','false']))
    ld.add_action(DeclareLaunchArgument(name = "rviz_config", default_value=default_rviz_config_path, 
                                        description="Absolut path to rviz config file"))

    ld.add_action(Node(
        package= "rviz2",
        executable="rviz2",
        arguments=["use_sim_time:=true",'-d', LaunchConfiguration('rviz_config')],
        output = "screen",
        condition = IfCondition(LaunchConfiguration('rviz'))
    ))


    # join state publisher
    ld.add_action(DeclareLaunchArgument(name="jsp", default_value="false", choices=['false','true'], 
                                        description= "Flag to enabel join state publisher gui"))
    
    ld.add_action(Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        condition = IfCondition(LaunchConfiguration("jsp"))
    ))


    # robot state publisher 
    ld.add_action(DeclareLaunchArgument(name="rsp", default_value="true", choices=["true","false"],
                                        description="Flag to enabel robot state publisher"))

    ld.add_action(DeclareLaunchArgument(name = "path_to_urdf", default_value = path_to_xacro))

    ld.add_action(DeclareLaunchArgument(name = "urdf_package", default_value =  xacro_package ))

    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([this_package_share, 'launch', 'robot_state_publisher.launch.py']),
        launch_arguments={
            "urdf_package": LaunchConfiguration('urdf_package'),
            "path_to_urdf": LaunchConfiguration('path_to_urdf'),
            "use_sim_time": 'true'
        }.items(),
        condition = IfCondition(LaunchConfiguration("rsp"))
    ))

    # gazebo launch
    

    ld.add_action(IncludeLaunchDescription(
        PathJoinSubstitution([FindPackageShare('ros_gz_sim'), "launch", 'gz_sim.launch.py']),
        # launch_arguments={ 'gz_args':PathJoinSubstitution([this_package_share, 'worlds', 'building_robot.sdf']) }.items()
        launch_arguments={ 'gz_args':"empty.sdf", "on_exit_shutdown":'true'}.items() 
    ))

    # gazebo spawn robots
        
    ld.add_action(Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'my_bot',
                                   '-z', '0.1'],
                        output='screen'))

    # gazebo bridgs
    ld.add_action(Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['depth_camera'],
        output='screen'
    ))
    # os.path.join(get_package_share_directory(package_name),'config','gz_bridge.yaml')
    ld.add_action(Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments={
            '--ros-args':'',
            '-p':'',
            'config_file:=':bridge_params
        }.items()
        
    ))

    return ld

