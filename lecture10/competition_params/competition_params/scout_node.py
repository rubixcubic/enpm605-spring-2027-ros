"""Lecture 7's scout, with its top speed as a parameter (Lecture 10)."""

from rcl_interfaces.msg import FloatingPointRange, ParameterDescriptor
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

SPEED_LIMIT_MPS = 3.0  # Highest top speed allowed (chosen)


class ScoutNode(Node):
    """Declares two parameters and logs the top speed once per second."""

    def __init__(self):
        super().__init__('scout')
        speed = ParameterDescriptor(
            description='Top speed, in m/s',
            floating_point_range=[FloatingPointRange(
                from_value=0.0, to_value=SPEED_LIMIT_MPS)])
        name = ParameterDescriptor(
            description='Name of the robot',
            read_only=True)  # Lecture 6, rule 5: names do not change
        self.declare_parameter('max_speed_mps', 2.0, speed)
        self.declare_parameter('robot_name', 'Scout', name)
        self._name = self.get_parameter('robot_name').value
        self._speed = self.get_parameter('max_speed_mps').value  # Once
        self._timer = self.create_timer(1.0, self._report)

    def _report(self):
        self.get_logger().info(f'{self._name}: {self._speed} m/s')


class LiveScoutNode(ScoutNode):
    """The same node, told when a parameter has changed."""

    def __init__(self):
        super().__init__()
        self.add_post_set_parameters_callback(self._on_parameters_set)

    def _on_parameters_set(self, parameters):
        for parameter in parameters:  # Each parameter just set
            if parameter.name == 'max_speed_mps':
                self._speed = parameter.value


def run(node):
    """Spin the node until Ctrl+C (Lecture 8's main())."""
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


def main(args=None):
    rclpy.init(args=args)
    run(ScoutNode())


def live(args=None):
    rclpy.init(args=args)
    run(LiveScoutNode())
