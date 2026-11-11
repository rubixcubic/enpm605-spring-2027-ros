"""A team of two robots: robot_launch.py, included twice (Lecture 9)."""

from launch import LaunchDescription
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_launch = PathJoinSubstitution([
        FindPackageShare('competition_bringup'), 'launch',
        'robot_launch.py'])
    # Each include is in a group, so its arguments stay in that group
    robot1 = GroupAction([IncludeLaunchDescription(
        robot_launch, launch_arguments={'robot': 'robot1'}.items())])
    robot2 = GroupAction([IncludeLaunchDescription(
        robot_launch, launch_arguments={
            'robot': 'robot2', 'with_monitor': 'false'}.items())])
    return LaunchDescription([robot2, robot1])
