"""A settings node for robot1, with a parameter set at start (Lecture 9)."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    settings = Node(
        package='demo_nodes_cpp',
        executable='parameter_blackboard',  # Accepts any parameter
        namespace='robot1',
        parameters=[{'max_speed_mps': 2.0}],  # Lecture 7's scout speed
    )
    return LaunchDescription([settings])
