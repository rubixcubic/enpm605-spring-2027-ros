"""Log the robot's pose and speed from /odom once per second (Lecture 11)."""

import math

from competition_motion.pose_tools import yaw_from_quaternion
from nav_msgs.msg import Odometry
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class OdomReader(Node):
    """Keeps the last odometry message and logs it once per second."""

    def __init__(self):
        super().__init__('odom_reader')
        self._last = None
        self._subscription = self.create_subscription(
            Odometry, 'odom', self._on_odom, 10)
        self._timer = self.create_timer(1.0, self._report)

    def _on_odom(self, msg):
        self._last = msg

    def _report(self):
        if self._last is None:
            return
        pose = self._last.pose.pose
        twist = self._last.twist.twist
        yaw = math.degrees(yaw_from_quaternion(pose.orientation))
        self.get_logger().info(  # m, m, degrees, m/s, rad/s
            f'x={pose.position.x:.2f} y={pose.position.y:.2f} '
            f'yaw={yaw:.1f} v={twist.linear.x:.2f} w={twist.angular.z:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = OdomReader()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    except Exception:  # Ctrl+C can also end spin() with an RCLError
        if rclpy.ok():  # ROS 2 still running: a real error
            raise
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
