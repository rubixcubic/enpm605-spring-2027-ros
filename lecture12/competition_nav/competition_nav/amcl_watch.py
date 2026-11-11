"""Log how spread out AMCL's particles are, at each update (Lecture 12)."""

import math
import statistics

from nav2_msgs.msg import ParticleCloud
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data


class AmclWatch(Node):
    """Logs the size and the spread of each particle cloud AMCL sends."""

    def __init__(self):
        super().__init__('amcl_watch')
        # AMCL publishes the cloud best effort: subscribe the same way
        self._sub = self.create_subscription(
            ParticleCloud, 'particle_cloud', self._on_cloud,
            qos_profile_sensor_data)

    def _on_cloud(self, msg):
        xs = [p.pose.position.x for p in msg.particles]
        ys = [p.pose.position.y for p in msg.particles]
        mx, my = statistics.fmean(xs), statistics.fmean(ys)
        # Spread: the root mean square distance of the particles to their mean
        spread = math.hypot(statistics.pstdev(xs), statistics.pstdev(ys))
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        self.get_logger().info(  # s of simulation time; m
            f't={t:.1f} n={len(xs)} mean=({mx:.2f}, {my:.2f}) '
            f'spread={spread:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = AmclWatch()
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
