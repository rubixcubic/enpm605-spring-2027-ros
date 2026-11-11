"""Publish the goal as a frame of its own, once (Lecture 11)."""

import math

from competition_motion.pose_tools import quaternion_from_yaw
from geometry_msgs.msg import TransformStamped
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster


class GoalBroadcaster(Node):
    """Sends the static transform from odom to goal at start."""

    def __init__(self):
        super().__init__('goal_broadcaster')
        self.declare_parameter('x', 2.0)  # In odom, m (chosen)
        self.declare_parameter('y', 1.0)
        self.declare_parameter('yaw_deg', 0.0)
        self._broadcaster = StaticTransformBroadcaster(self)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'  # The parent frame
        t.child_frame_id = 'goal'  # The frame this node adds
        t.transform.translation.x = self.get_parameter('x').value
        t.transform.translation.y = self.get_parameter('y').value
        yaw = math.radians(self.get_parameter('yaw_deg').value)
        r = t.transform.rotation
        r.x, r.y, r.z, r.w = quaternion_from_yaw(yaw)
        self._broadcaster.sendTransform(t)
        self.get_logger().info(
            f'Sent odom -> goal: x={t.transform.translation.x}, '
            f'y={t.transform.translation.y}, yaw={math.degrees(yaw)} deg')


def main(args=None):
    rclpy.init(args=args)
    node = GoalBroadcaster()
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
