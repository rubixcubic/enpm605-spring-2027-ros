"""Gazebo Harmonic, a TurtleBot3 Waffle in the arena, and RViz2 (Lecture 11)."""

# The robot, its bridge to ROS 2, and its URDF come from nav2_minimal_tb3_sim,
# the package that Nav2's own simulation uses (Lecture 12).

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
    here = get_package_share_directory('competition_motion')
    tb3 = get_package_share_directory('nav2_minimal_tb3_sim')
    world = os.path.join(here, 'worlds', 'arena.sdf')
    with open(os.path.join(tb3, 'urdf', 'turtlebot3_waffle.urdf')) as f:
        robot_description = f.read()  # The robot's links and joints
    gui = LaunchConfiguration('gui')
    rviz = LaunchConfiguration('rviz')
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true',
                              description='Open the Gazebo window'),
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Open RViz2'),
        # Spawn the robot at (0, 0), bridge its topics to ROS 2, and tell
        # Gazebo where its meshes are (first, so the server sees it)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(tb3, 'launch', 'spawn_tb3.launch.py')),
            launch_arguments={'x_pose': '0.0', 'y_pose': '0.0'}.items()),
        # The simulation itself (-s: server, -r: run at once)
        ExecuteProcess(cmd=['gz', 'sim', '-r', '-s', world]),
        # The Gazebo window, a client of the server (-g: GUI only)
        ExecuteProcess(cmd=['gz', 'sim', '-g'], condition=IfCondition(gui)),
        # Publish the transforms between the robot's links
        Node(package='robot_state_publisher',
             executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description,
                          'use_sim_time': True}]),
        Node(package='rviz2', executable='rviz2',
             arguments=['-d', os.path.join(here, 'rviz', 'arena.rviz')],
             parameters=[{'use_sim_time': True}],
             condition=IfCondition(rviz)),
    ])
