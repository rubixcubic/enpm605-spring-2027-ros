"""Subscribe to the battery level and report the status (Lecture 8)."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import BatteryState

LOW_BATTERY_PCT = 10  # Rule 3 of Lecture 6, chosen for that example


class BatteryMonitor(Node):
    """Logs each battery level it receives, with the robot's status."""

    def __init__(self):
        super().__init__('battery_monitor')
        self._subscription = self.create_subscription(
            BatteryState, 'battery', self._on_battery, 10)

    def _on_battery(self, msg):
        level = round(msg.percentage * 100)  # A whole percent (rule 1)
        if level < LOW_BATTERY_PCT:
            self.get_logger().warning(f'{level}%: needs_recharge')
        else:
            self.get_logger().info(f'{level}%: active')


def main(args=None):
    rclpy.init(args=args)
    node = BatteryMonitor()
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
