"""Two robots, each with its battery nodes in its own namespace (Lecture 9)."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    nodes = []
    for robot in ['robot1', 'robot2']:  # A launch file is Python code
        nodes.append(Node(package='competition_nodes', namespace=robot,
                          executable='battery_publisher'))
        nodes.append(Node(package='competition_nodes', namespace=robot,
                          executable='battery_monitor'))
    return LaunchDescription(nodes)
