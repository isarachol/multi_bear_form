import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node

import xacro

def launch_setup(context, *args, **kwargs):

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    robot_name = LaunchConfiguration('robot_name').perform(context)

    # Process the URDF file from XACRO
    my_package_name = 'multi_bear_form'
    pkg_path = os.path.join(get_package_share_directory(my_package_name))
    xacro_file_path = os.path.join(pkg_path,'description','robot_car.urdf.xacro')
    
    robot_description_topic_name = "/" + robot_name + "/robot_description"
    joint_state_topic_name = "/" + robot_name + "/joint_states" # may not use?
    robot_state_publisher_name = robot_name + "_robot_state_publisher"
    # robot_description_config = Command(['xacro ', xacro_file,
    #                                     ' use_ros2_control:=', use_ros2_control])
    robot_description_config = xacro.process_file(xacro_file_path, mappings={'robot_name': robot_name}).toxml()

    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time,}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name=robot_state_publisher_name,
        output='screen',
        parameters=[params],
        remappings=[("/robot_description", robot_description_topic_name),
                    ("/joint_states", joint_state_topic_name)]
    )
    return [node_robot_state_publisher]

def generate_launch_description():

    # params2 = {'robot_description2': robot_description_config, 'use_sim_time': use_sim_time}
    # node_robot_state_publisher2 = Node(
    #     package='robot_state_publisher',
    #     executable='robot_state_publisher',
    #     name='robot_state_publisher2',
    #     output='screen',
    #     parameters=[params2]
    # )

    # rviz_config = os.path.join(
    #     get_package_share_directory('bearing_formation_control'), 'config',
    #     'xmobile_agent.rviz'
    #     )
    
    # teleop_node = Node(
    #     package='teleop_twist_keyboard',
    #     executable='teleop_twist_keyboard',
    #     name='teleop_twist_keyboard',
    #     remappings=[('/cmd_vel', 'diff_cont/cmd_vel_unstamped')],
    # )


    # use_ros2_control = LaunchConfiguration('use_ros2_control')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        DeclareLaunchArgument(
            'use_ros2_control',
            default_value='true',
            description='Use ros2_control if true'),
        DeclareLaunchArgument(
            'robot_name',
            default_value='robot_1',
            description='Give name of multiple robots',),
        OpaqueFunction(function = launch_setup), # need to study this function
        # node_robot_state_publisher2,
        # Node(
        #     package='bearing_formation_control',
        #     executable='single_state_publisher',
        #     name='single_state_publisher',
        #     output='screen'),
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     arguments=['-d', rviz_config],
        # ),
        # teleop_node,
    ])
