"""Gazebo Harmonic, a TurtleBot3 Waffle in Nav2's sandbox, and RViz2 (Lecture 12)."""

# Lecture 11's arena_launch.py with another world: the robot, its bridge
# to ROS 2, and its URDF come from nav2_minimal_tb3_sim; RViz2 opens Nav2's
# own settings file, which shows the map, the costmaps, and the plan.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess,
                            IncludeLaunchDescription)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    here = get_package_share_directory('competition_nav')
    tb3 = get_package_share_directory('nav2_minimal_tb3_sim')
    nav2 = get_package_share_directory('nav2_bringup')
    world = os.path.join(here, 'worlds', 'sandbox.sdf')
    with open(os.path.join(tb3, 'urdf', 'turtlebot3_waffle.urdf')) as f:
        robot_description = f.read()  # The robot's links and joints
    gui = LaunchConfiguration('gui')
    rviz = LaunchConfiguration('rviz')
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true',
                              description='Open the Gazebo window'),
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Open RViz2'),
        # Spawn the robot at (-2.0, -0.5) in Gazebo's world, facing x
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3, 'launch', 'spawn_tb3.launch.py')),
            launch_arguments={'x_pose': '-2.0', 'y_pose': '-0.5'}.items()),
        ExecuteProcess(cmd=['gz', 'sim', '-r', '-s', world]),
        ExecuteProcess(cmd=['gz', 'sim', '-g'], condition=IfCondition(gui)),
        Node(package='robot_state_publisher',
             executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description,
                          'use_sim_time': True}]),
        Node(package='rviz2', executable='rviz2',
             arguments=['-d', os.path.join(nav2, 'rviz',
                                           'nav2_default_view.rviz')],
             parameters=[{'use_sim_time': True}],
             condition=IfCondition(rviz)),
    ])
