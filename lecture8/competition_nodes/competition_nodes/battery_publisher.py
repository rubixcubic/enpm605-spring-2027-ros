"""Publish a robot's battery level as it drains (Lecture 8)."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import BatteryState

DRAIN_PCT_PER_MIN = 2  # Rule 4 of Lecture 6, chosen for that example
# One message per second stands for one minute (chosen for this example)


class BatteryPublisher(Node):
    """Publishes the battery level once per second."""

    def __init__(self):
        super().__init__('battery_publisher')
        self._battery = 16  # Percent, chosen to cross 10% soon
        self._publisher = self.create_publisher(
            BatteryState, 'battery', 10)  # Topic name, queue size
        self._timer = self.create_timer(1.0, self._publish_battery)

    def _publish_battery(self):
        msg = BatteryState()
        msg.percentage = self._battery / 100  # The message uses 0 to 1
        msg.present = True
        self._publisher.publish(msg)
        self.get_logger().info(f'Published {self._battery}%')
        self._battery = max(0, self._battery - DRAIN_PCT_PER_MIN)


def main(args=None):
    rclpy.init(args=args)
    node = BatteryPublisher()
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
