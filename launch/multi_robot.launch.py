import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, OpaqueFunction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

# def launch_setup(context, *args, **kwargs):
#     '''
#     Will be called from generate_launch_description
#     '''
#     robot_name = LaunchConfiguration('robot_name').perform(context)
#     robot_xyz = LaunchConfiguration('robot_xyz').perform(context)
#     robot_rpy = LaunchConfiguration('robot_rpy').perform(context)
#     package_name='multi_bear_form' #<--- CHANGE ME
#     robot_state_publisher = IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource([os.path.join(
#                     get_package_share_directory(package_name),'launch','robot_state_publisher.launch.py'
#                 )]), launch_arguments={'use_sim_time': 'true',
#                                        'use_ros2_control': 'true',
#                                        'robot_name': robot_name,}.items()
#     )

#     gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo.yaml')
#     gazebo = IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource([os.path.join(
#                     get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
#                     launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items())
    
#     robot_description_topic_name = "/" + robot_name + "/robot_description"
#     # robot_state_publisher_name = robot_name + "/robot_state_publisher"

#     location = robot_xyz.split(" ")
#     orientation = robot_rpy.split(" ")
#     # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
#     spawn_entity = Node(package='gazebo_ros',
#                         executable='spawn_entity.py',
#                         name='robot_spawn_entity',
#                         arguments=['-topic', robot_description_topic_name,
#                                    '-entity', robot_name,
#                                    '-x', location[0], '-y', location[1], '-z', location[2],
#                                    '-R', orientation[0], '-P', orientation[1], '-Y', orientation[2]],
#                         # remappings=[("/robot_state_publisher", robot_state_publisher_name)],
#                         namespace=robot_name,
#                         output='screen')

#     # Run diff drive controller
#     diff_drive_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         name="spawn_controller_diff_cont",
#         arguments=["diff_cont"],
#         namespace=robot_name,
#     )

#     # # Run joint broad controller
#     joint_broad_spawner = Node(
#         package="controller_manager",
#         executable="spawner",
#         name="spawn_controller_joint_broad",
#         arguments=["joint_broad"],
#         namespace=robot_name,
#     )

#     return [robot_state_publisher,
#             gazebo,
#             spawn_entity,
#             diff_drive_spawner,
#             joint_broad_spawner,]


def generate_launch_description():
    '''
    Launch one robot in any random pose with a custom name. For now the name can only be robot_1 and robot_2.
    '''
    package_name = 'multi_bear_form'
    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo.yaml')
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items())
    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!
    sim_gazebo1 = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','sim_gazebo.launch.py'
                )]), launch_arguments={'use_sim_time': 'true',
                                       'use_ros2_control': 'true',
                                       'robot_name': 'robot_1',
                                       'robot_xyz': '0. 2. 0.',}.items()
    )

    sim_gazebo2 = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','sim_gazebo.launch.py'
                )]), launch_arguments={'use_sim_time': 'true',
                                       'use_ros2_control': 'true',
                                       'robot_name': 'robot_2',
                                       'robot_xyz': '2. 0. 0.',}.items()
    )

    return LaunchDescription([
        gazebo,
        sim_gazebo1,
        sim_gazebo2,
    ])
