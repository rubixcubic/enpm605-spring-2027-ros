"""The sandbox, plus SLAM Toolbox building a map (Lecture 12)."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    here = get_package_share_directory('competition_nav')
    slam = get_package_share_directory('slam_toolbox')
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(here, 'launch', 'sandbox_launch.py')),
            launch_arguments={'gui': LaunchConfiguration('gui'),
                              'rviz': LaunchConfiguration('rviz')}.items()),
        # SLAM Toolbox with its own parameters file for online mapping:
        # it publishes /map and the transform map -> odom
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(slam, 'launch', 'online_async_launch.py')),
            launch_arguments={'use_sim_time': 'true'}.items()),
    ])
