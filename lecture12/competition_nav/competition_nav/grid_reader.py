"""Read an occupancy grid from a topic and count its cells (Lecture 12)."""

from collections import Counter

from nav_msgs.msg import OccupancyGrid
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy


class GridReader(Node):
    """Logs the size of each grid it receives, and its cells by value."""

    def __init__(self):
        super().__init__('grid_reader')
        self.declare_parameter('topic', 'map')
        # A map is published once, or seldom: ask for the last one sent
        # before this node started (Lecture 10)
        qos = QoSProfile(depth=1,
                         reliability=ReliabilityPolicy.RELIABLE,
                         durability=DurabilityPolicy.TRANSIENT_LOCAL)
        self._sub = self.create_subscription(
            OccupancyGrid, self.get_parameter('topic').value,
            self._on_grid, qos)

    def _on_grid(self, msg):
        info = msg.info
        origin = info.origin.position
        self.get_logger().info(
            f'{info.width} x {info.height} cells of {info.resolution:.2f} m, '
            f'origin ({origin.x:.2f}, {origin.y:.2f})')
        counts = Counter(msg.data)  # Cell value: how many cells
        other = sum(n for v, n in counts.items() if v not in (-1, 0, 100))
        self.get_logger().info(
            f'free {counts[0]}, occupied {counts[100]}, '
            f'unknown {counts[-1]}, other {other}')


def main(args=None):
    rclpy.init(args=args)
    node = GridReader()
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
