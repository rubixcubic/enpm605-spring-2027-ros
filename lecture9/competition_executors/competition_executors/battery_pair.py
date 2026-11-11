"""Lecture 8's battery publisher and monitor in one process (Lecture 9)."""

from competition_nodes.battery_monitor import BatteryMonitor
from competition_nodes.battery_publisher import BatteryPublisher
import rclpy
from rclpy.executors import ExternalShutdownException, SingleThreadedExecutor


def main(args=None):
    rclpy.init(args=args)
    publisher = BatteryPublisher()
    monitor = BatteryMonitor()
    executor = SingleThreadedExecutor()
    executor.add_node(publisher)  # One executor, one thread, two nodes
    executor.add_node(monitor)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    except Exception:  # Ctrl+C can also end spin() with an RCLError
        if rclpy.ok():  # ROS 2 still running: a real error
            raise
    finally:
        executor.shutdown()
        monitor.destroy_node()
        publisher.destroy_node()
        rclpy.try_shutdown()
