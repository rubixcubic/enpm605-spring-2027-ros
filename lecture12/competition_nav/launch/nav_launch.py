"""The sandbox, plus Nav2 on a saved map: map_server, AMCL, and the servers (Lecture 12)."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    here = get_package_share_directory('competition_nav')
    nav2 = get_package_share_directory('nav2_bringup')
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument(
            'map', default_value=os.path.join(here, 'maps', 'sandbox.yaml'),
            description='The map file (yaml) to load'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(here, 'launch', 'sandbox_launch.py')),
            launch_arguments={'gui': LaunchConfiguration('gui'),
                              'rviz': LaunchConfiguration('rviz')}.items()),
        # Nav2's own bringup with its default parameters file
        # (nav2_bringup/params/nav2_params.yaml): map_server and AMCL
        # (localization), then the planner, controller, behavior, and
        # BT navigator servers (navigation)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2, 'launch', 'bringup_launch.py')),
            launch_arguments={'map': LaunchConfiguration('map'),
                              'use_sim_time': 'true'}.items()),
    ])
