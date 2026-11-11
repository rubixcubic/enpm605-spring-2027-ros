"""Watch robot2's battery from outside its namespace (Lecture 9)."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    watch = Node(
        package='competition_nodes',
        executable='battery_monitor',
        name='robot2_watch',  # Replaces the name written in the code
        remappings=[('battery', '/robot2/battery')],
    )
    return LaunchDescription([watch])
