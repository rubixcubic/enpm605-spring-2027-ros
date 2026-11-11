"""An include's arguments reach the next include (Lecture 9)."""

# robot2 is included first, with with_monitor false; robot1 is included
# next and does not set with_monitor. Run it by its path, from the ROS
# repository's folder: ros2 launch lecture9/errors/team_leak_launch.py

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    robot_launch = PathJoinSubstitution([
        FindPackageShare('competition_bringup'), 'launch',
        'robot_launch.py'])
    robot2 = IncludeLaunchDescription(
        robot_launch, launch_arguments={
            'robot': 'robot2', 'with_monitor': 'false'}.items())
    robot1 = IncludeLaunchDescription(  # Does not set with_monitor
        robot_launch, launch_arguments={'robot': 'robot1'}.items())
    return LaunchDescription([robot2, robot1])
