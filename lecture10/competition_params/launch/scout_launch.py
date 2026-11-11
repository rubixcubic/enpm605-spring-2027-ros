"""Start the scout with the parameters of config/scout.yaml."""

from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    config = PathJoinSubstitution([
        FindPackageShare('competition_params'), 'config', 'scout.yaml'])
    scout = Node(package='competition_params', executable='scout_node',
                 parameters=[config])  # A file, not a dictionary
    return LaunchDescription([scout])
