"""One robot: its battery nodes in a namespace you choose (Lecture 9)."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, PushROSNamespace


def generate_launch_description():
    robot = LaunchConfiguration('robot')
    with_monitor = LaunchConfiguration('with_monitor')
    return LaunchDescription([
        DeclareLaunchArgument('robot', default_value='robot1',
                              description='Namespace of the robot'),
        DeclareLaunchArgument('with_monitor', default_value='true',
                              description='Start the battery monitor'),
        GroupAction([
            PushROSNamespace(robot),  # For every node in this group
            Node(package='competition_nodes',
                 executable='battery_publisher'),
            Node(package='competition_nodes',
                 executable='battery_monitor',
                 condition=IfCondition(with_monitor)),
        ]),
    ])
