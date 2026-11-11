"""Tell AMCL where the robot starts, then wait for its answer (Lecture 12)."""

import math

from competition_motion.pose_tools import (quaternion_from_yaw,
                                           yaw_from_quaternion)
from geometry_msgs.msg import PoseWithCovarianceStamped
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy


class InitialPose(Node):
    """Publishes a pose on /initialpose until AMCL reports one."""

    def __init__(self):
        super().__init__('initial_pose')
        self.declare_parameter('x', 0.0)  # In map, m: where SLAM started
        self.declare_parameter('y', 0.0)
        self.declare_parameter('yaw_deg', 0.0)
        self.declare_parameter('sigma_m', 0.5)  # How unsure (chosen)
        self.declare_parameter('sigma_deg', 15.0)
        self._pub = self.create_publisher(
            PoseWithCovarianceStamped, 'initialpose', 10)
        # AMCL publishes its pose transient local: ask for the last one
        qos = QoSProfile(depth=1,
                         reliability=ReliabilityPolicy.RELIABLE,
                         durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self._sub = self.create_subscription(
            PoseWithCovarianceStamped, 'amcl_pose', self._on_amcl, qos)
        self._sent = False
        self._timer = self.create_timer(2.0, self._send)  # Retry (chosen)

    def _send(self):
        if self._pub.get_subscription_count() == 0:
            return  # AMCL is not up yet
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        p = msg.pose.pose
        p.position.x = self.get_parameter('x').value
        p.position.y = self.get_parameter('y').value
        yaw = math.radians(self.get_parameter('yaw_deg').value)
        r = p.orientation
        r.x, r.y, r.z, r.w = quaternion_from_yaw(yaw)
        cov = [0.0] * 36  # 6 x 6, row by row: x, y, z, roll, pitch, yaw
        cov[0] = cov[7] = self.get_parameter('sigma_m').value ** 2
        cov[35] = math.radians(self.get_parameter('sigma_deg').value) ** 2
        msg.pose.covariance = cov
        self._pub.publish(msg)
        self._sent = True
        self.get_logger().info(
            f'Sent initial pose: x={p.position.x:.2f} y={p.position.y:.2f} '
            f'yaw={math.degrees(yaw):.1f}')

    def _on_amcl(self, msg):
        if not self._sent:
            return  # A pose from before this node's message
        p = msg.pose.pose
        yaw = math.degrees(yaw_from_quaternion(p.orientation))
        self.get_logger().info(
            f'AMCL: x={p.position.x:.2f} y={p.position.y:.2f} yaw={yaw:.1f}')
        rclpy.shutdown()  # AMCL has the pose: ends spin()


def main(args=None):
    rclpy.init(args=args)
    node = InitialPose()
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
