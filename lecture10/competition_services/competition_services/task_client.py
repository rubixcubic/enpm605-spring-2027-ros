"""Send one AssignTask request and print the reply (Lecture 10)."""

# Run: ros2 run competition_services task_client "pick widget" 5

import sys

from competition_interfaces.srv import AssignTask
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.utilities import remove_ros_args


def main(args=None):
    rclpy.init(args=args)
    task, minutes = remove_ros_args(sys.argv)[1:3]  # Lecture 9
    node = rclpy.create_node('task_client')
    client = node.create_client(AssignTask, 'assign_task')
    try:
        while not client.wait_for_service(timeout_sec=1.0):
            node.get_logger().info('Waiting for assign_task')
        request = AssignTask.Request(task=task, minutes=int(minutes))
        future = client.call_async(request)  # Sends it, does not wait
        rclpy.spin_until_future_complete(node, future)  # Waits here
        reply = future.result()
        node.get_logger().info(
            f'accepted: {reply.accepted}, battery: {reply.battery_pct}%, '
            f'{reply.message}')
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    except Exception:  # Ctrl+C can also end spin() with an RCLError
        if rclpy.ok():  # ROS 2 still running: a real error
            raise
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
