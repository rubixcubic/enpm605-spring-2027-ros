"""Print the global costmap's costs along a line of cells (Lecture 12)."""

from competition_nav.grid_math import cell_to_point, point_to_cell
from nav2_msgs.msg import Costmap
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class CostProbe(Node):
    """Logs the costs of n cells, from a start point toward +x, once."""

    def __init__(self):
        super().__init__('cost_probe')
        self.declare_parameter('x', 2.0)  # Start point in map, m (chosen)
        self.declare_parameter('y', 0.5)
        self.declare_parameter('cells', 16)
        # The raw costs, 0 to 255, as the planner sees them
        self._sub = self.create_subscription(
            Costmap, 'global_costmap/costmap_raw', self._on_costmap, 10)

    def _on_costmap(self, msg):
        m = msg.metadata
        origin = (m.origin.position.x, m.origin.position.y)
        col, row = point_to_cell(self.get_parameter('x').value,
                                 self.get_parameter('y').value,
                                 origin, m.resolution)
        for k in range(self.get_parameter('cells').value):
            x, y = cell_to_point(col + k, row, origin, m.resolution)
            cost = msg.data[row * m.size_x + col + k]  # Row by row
            self.get_logger().info(f'cell ({col + k}, {row}) at '
                                   f'x={x:.3f} y={y:.3f}: cost {cost}')
        rclpy.shutdown()  # One costmap is enough: ends spin()


def main(args=None):
    rclpy.init(args=args)
    node = CostProbe()
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
