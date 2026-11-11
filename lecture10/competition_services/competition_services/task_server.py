"""A robot that accepts or refuses tasks, as a service (Lecture 10)."""

from competition_interfaces.srv import AssignTask
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

LOW_BATTERY_PCT = 10  # Rule 3 of Lecture 6, chosen for that example
DRAIN_PCT_PER_MIN = 2  # Rule 4 of Lecture 6, chosen for that example


class TaskServer(Node):
    """Answers each AssignTask request with Lecture 6's rules 3 and 4."""

    def __init__(self):
        super().__init__('task_server')
        self.declare_parameter('battery_pct', 30)  # Percent, chosen
        self._battery = self.get_parameter('battery_pct').value
        self._service = self.create_service(
            AssignTask, 'assign_task', self._assign_task)

    def _assign_task(self, request, response):
        cost = DRAIN_PCT_PER_MIN * request.minutes
        if self._battery < LOW_BATTERY_PCT:  # Rule 3
            response.message = 'needs_recharge'
        elif cost > self._battery:
            response.message = f'needs {cost}%, has {self._battery}%'
        else:  # Rule 4: the task uses 2% per minute
            self._battery -= cost
            response.accepted = True
            response.message = 'done'
        response.battery_pct = self._battery
        self.get_logger().info(
            f'{request.task} ({request.minutes} min): {response.message}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = TaskServer()
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
