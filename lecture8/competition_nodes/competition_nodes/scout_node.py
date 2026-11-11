"""Lecture 7's ScoutNode, run as a node of a package (Lecture 8)."""

import rclpy
from rclpy.node import Node


class ScoutNode(Node):
    """A node for the competition's scout robot."""

    def __init__(self):
        super().__init__('scout')  # Node.__init__ takes the node's name
        self.max_speed_mps = 2.0  # Chosen for this example (Lecture 7)
        self.get_logger().info(f'Top speed {self.max_speed_mps} m/s')


def main(args=None):
    rclpy.init(args=args)
    node = ScoutNode()
    node.destroy_node()
    rclpy.shutdown()
