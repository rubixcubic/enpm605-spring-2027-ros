"""Send one NavigateToPose goal to Nav2 and log its progress (Lecture 12)."""

import math

from action_msgs.msg import GoalStatus
from competition_motion.pose_tools import quaternion_from_yaw
from nav2_msgs.action import NavigateToPose
import rclpy
from rclpy.action import ActionClient
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

STATUS = {GoalStatus.STATUS_SUCCEEDED: 'SUCCEEDED',
          GoalStatus.STATUS_CANCELED: 'CANCELED',
          GoalStatus.STATUS_ABORTED: 'ABORTED'}


class NavClient(Node):
    """Sends a goal pose in the map frame; logs feedback each second."""

    def __init__(self):
        super().__init__('nav_client')
        self.declare_parameter('x', 3.6)  # Task site, map frame, m (chosen)
        self.declare_parameter('y', 1.0)
        self.declare_parameter('yaw_deg', 0.0)
        self._last_s = -1
        self._time_s = 0.0  # Navigation time of the last feedback
        self._client = ActionClient(
            self, NavigateToPose, 'navigate_to_pose')
        self._client.wait_for_server()
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.pose.position.x = self.get_parameter('x').value
        goal.pose.pose.position.y = self.get_parameter('y').value
        yaw = math.radians(self.get_parameter('yaw_deg').value)
        r = goal.pose.pose.orientation
        r.x, r.y, r.z, r.w = quaternion_from_yaw(yaw)
        future = self._client.send_goal_async(
            goal, feedback_callback=self._on_feedback)
        future.add_done_callback(self._on_goal_response)

    def _on_goal_response(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal refused')
            rclpy.shutdown()  # Ends spin(): nothing more will come
            return
        self.get_logger().info('Goal accepted')
        goal_handle.get_result_async().add_done_callback(self._on_result)

    def _on_feedback(self, feedback_msg):
        f = feedback_msg.feedback
        s = f.navigation_time.sec  # Simulation time since the goal started
        self._time_s = s + f.navigation_time.nanosec / 1e9
        if s == self._last_s:
            return  # Log once per second of navigation time
        self._last_s = s
        p = f.current_pose.pose.position
        self.get_logger().info(
            f't={s} s at ({p.x:.2f}, {p.y:.2f}): '
            f'{f.distance_remaining:.2f} m to go, '
            f'recoveries {f.number_of_recoveries}')

    def _on_result(self, future):
        reply = future.result()  # The status and the result
        self.get_logger().info(
            f'Result: {STATUS.get(reply.status, reply.status)} after '
            f'{self._time_s:.1f} s, error_code={reply.result.error_code}')
        rclpy.shutdown()  # Ends spin(): the goal is over


def main(args=None):
    rclpy.init(args=args)
    node = NavClient()
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
