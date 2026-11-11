"""A node written as a script, without a class (Lecture 8)."""

import rclpy


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('minimal_node')  # The node's name
    node.get_logger().info('Hello from ROS 2')
    node.destroy_node()
    rclpy.shutdown()
