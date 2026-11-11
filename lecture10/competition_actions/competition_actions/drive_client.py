"""Send a DriveToGoal goal, log the feedback, maybe cancel (Lecture 10)."""

from action_msgs.msg import GoalStatus
from competition_interfaces.action import DriveToGoal
import rclpy
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

STATUS = {GoalStatus.STATUS_SUCCEEDED: 'SUCCEEDED',
          GoalStatus.STATUS_CANCELED: 'CANCELED',
          GoalStatus.STATUS_ABORTED: 'ABORTED'}


class DriveClient(Node):
    """Sends one goal; cancels it after cancel_after feedback messages."""

    def __init__(self):
        super().__init__('drive_client')
        self.declare_parameter('distance_m', 5.0)  # Chosen for this example
        self.declare_parameter('cancel_after', 0)  # 0: never cancel
        self._cancel_after = self.get_parameter('cancel_after').value
        self._feedback_count = 0
        self._goal_handle = None
        self._client = ActionClient(self, DriveToGoal, 'drive_to_goal')
        self._client.wait_for_server()
        goal = DriveToGoal.Goal(
            distance_m=self.get_parameter('distance_m').value)
        future = self._client.send_goal_async(
            goal, feedback_callback=self._on_feedback)
        future.add_done_callback(self._on_goal_response)

    def _on_goal_response(self, future):
        self._goal_handle = future.result()
        if not self._goal_handle.accepted:
            self.get_logger().info('Goal refused')
            rclpy.shutdown()  # Ends spin(): nothing more will come
            return
        self.get_logger().info('Goal accepted')
        result_future = self._goal_handle.get_result_async()
        result_future.add_done_callback(self._on_result)

    def _on_feedback(self, feedback_msg):
        remaining = feedback_msg.feedback.distance_remaining_m
        self.get_logger().info(f'Feedback: {remaining} m to go')
        self._feedback_count += 1
        if self._feedback_count == self._cancel_after:
            self.get_logger().info('Canceling the goal')
            self._goal_handle.cancel_goal_async()

    def _on_result(self, future):
        reply = future.result()  # The status and the result
        self.get_logger().info(
            f'Result: {STATUS[reply.status]}, '
            f'driven {reply.result.distance_driven_m} m')
        rclpy.shutdown()  # Ends spin(): the goal is over


def main(args=None):
    rclpy.init(args=args)
    node = DriveClient()
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
