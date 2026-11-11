"""Drive a route of waypoints with Lecture 11's controller (Lecture 12)."""

from competition_motion.go_to_goal import GoToGoal
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.parameter import Parameter

# A loop through the sandbox's corridors, in odom, m (chosen): the robot
# starts at (0, 0); the pillars are 1.1 m apart
ROUTE = [3.65, -0.05, 3.65, 1.05, 0.35, 1.05, 0.35, -0.05, 1.5, -0.05]


class RouteDriver(GoToGoal):
    """Moves the goal to the next waypoint when the robot is near."""

    def __init__(self):
        super().__init__('route_driver')
        self.declare_parameter('route', ROUTE)  # x1, y1, x2, y2, ...
        self.declare_parameter('pass_m', 0.15)  # Near enough (chosen)
        self._index = 0
        self._aim()

    def _aim(self):
        route = self.get_parameter('route').value
        self.set_parameters([
            Parameter('goal_x', value=route[2 * self._index]),
            Parameter('goal_y', value=route[2 * self._index + 1])])

    def errors(self):
        e = super().errors()
        last = len(self.get_parameter('route').value) // 2 - 1
        if e is not None and e[0] < self.get_parameter('pass_m').value \
                and self._index < last:
            self.get_logger().info(f'Waypoint {self._index + 1} passed')
            self._index += 1
            self._aim()
            e = super().errors()
        return e


def main(args=None):
    rclpy.init(args=args)
    node = RouteDriver()
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
