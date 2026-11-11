"""Start the battery monitor and the battery publisher (Lecture 9)."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    monitor = Node(package='competition_nodes',
                   executable='battery_monitor')
    publisher = Node(package='competition_nodes',
                     executable='battery_publisher')
    return LaunchDescription([monitor, publisher])
