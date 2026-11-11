"""Subscribe to a robot's status with the QoS its parameters choose."""

from competition_interfaces.msg import RobotStatus
from competition_qos.qos_choice import declare_qos
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

NAMES = {RobotStatus.ACTIVE: 'active',
         RobotStatus.NEEDS_RECHARGE: 'needs_recharge'}


class StatusMonitor(Node):
    """Logs each status it receives."""

    def __init__(self):
        super().__init__('status_monitor')
        qos = declare_qos(self)
        self._subscription = self.create_subscription(
            RobotStatus, 'status', self._on_status, qos)

    def _on_status(self, msg):
        self.get_logger().info(
            f'{msg.name}: {msg.battery_pct}%, {NAMES[msg.status]}')


def main(args=None):
    rclpy.init(args=args)
    node = StatusMonitor()
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
