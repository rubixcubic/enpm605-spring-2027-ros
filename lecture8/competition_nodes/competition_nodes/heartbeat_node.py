"""A node that stays alive and runs a timer callback (Lecture 8)."""

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class HeartbeatNode(Node):
    """Logs a numbered heartbeat once per second."""

    def __init__(self):
        super().__init__('heartbeat')
        self._count = 0
        # Call self._on_timer every 1.0 s (chosen for this example)
        self._timer = self.create_timer(1.0, self._on_timer)

    def _on_timer(self):
        self._count += 1
        self.get_logger().info(f'Heartbeat {self._count}')


def main(args=None):
    rclpy.init(args=args)
    node = HeartbeatNode()
    try:
        rclpy.spin(node)  # Runs callbacks until Ctrl+C
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    except Exception:  # Ctrl+C can also end spin() with an RCLError
        if rclpy.ok():  # ROS 2 still running: a real error
            raise
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
