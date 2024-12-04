# Not working yet
import os

# from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration, Command

from launch_ros.actions import Node

def generate_launch_description():

    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        remappings=[('/cmd_vel', 'diff_cont/cmd_vel_unstamped')],
    )

    return LaunchDescription([
        teleop_node,
    ])
