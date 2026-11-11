"""Publish a robot's status with a QoS chosen by parameters (Lecture 10)."""

from competition_interfaces.msg import RobotStatus
from competition_qos.qos_choice import declare_qos
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

LOW_BATTERY_PCT = 10  # Rule 3 of Lecture 6, chosen for that example
DRAIN_PCT = 2  # Rule 4 of Lecture 6: one message stands for one minute


class StatusPublisher(Node):
    """Publishes `count` messages, one every 0.5 s, then keeps running."""

    def __init__(self):
        super().__init__('status_publisher')
        qos = declare_qos(self)
        self.declare_parameter('count', 5)  # Chosen for this example
        self._left = self.get_parameter('count').value
        self._battery = 30  # Percent, chosen for this example
        self._publisher = self.create_publisher(RobotStatus, 'status', qos)
        self._timer = self.create_timer(0.5, self._publish_status)  # Chosen

    def _publish_status(self):
        if self._left == 0:
            return
        msg = RobotStatus(name='scout', battery_pct=self._battery)
        if self._battery < LOW_BATTERY_PCT:
            msg.status = RobotStatus.NEEDS_RECHARGE
        else:
            msg.status = RobotStatus.ACTIVE
        self._publisher.publish(msg)
        self.get_logger().info(f'Published {self._battery}%')
        self._battery -= DRAIN_PCT
        self._left -= 1


def main(args=None):
    rclpy.init(args=args)
    node = StatusPublisher()
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
