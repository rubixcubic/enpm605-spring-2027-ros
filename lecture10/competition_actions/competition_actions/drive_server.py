"""Drive a distance as an action, with feedback and cancel (Lecture 10)."""

import time

from competition_executors.controller_runs import spin_until_ctrl_c
from competition_interfaces.action import DriveToGoal
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
from rclpy.node import Node

STEP_S = 0.5  # Seconds between two feedback messages (chosen)


class DriveServer(Node):
    """Drives at max_speed_mps until the goal's distance is covered."""

    def __init__(self):
        super().__init__('drive_server')
        self.declare_parameter('max_speed_mps', 2.0)  # Lecture 7
        self._server = ActionServer(
            self, DriveToGoal, 'drive_to_goal',
            execute_callback=self._drive,
            goal_callback=self._check_goal,
            cancel_callback=self._check_cancel)

    def _check_goal(self, goal):
        if goal.distance_m <= 0.0:
            self.get_logger().info(f'Goal refused: {goal.distance_m} m')
            return GoalResponse.REJECT
        self.get_logger().info(f'Goal accepted: {goal.distance_m} m')
        return GoalResponse.ACCEPT

    def _check_cancel(self, goal_handle):
        self.get_logger().info('Cancel accepted')
        return CancelResponse.ACCEPT

    def _drive(self, goal_handle):
        speed = self.get_parameter('max_speed_mps').value
        distance = goal_handle.request.distance_m
        driven = 0.0
        while driven < distance:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info(f'Canceled after {driven} m')
                return DriveToGoal.Result(distance_driven_m=driven)
            time.sleep(STEP_S)  # Stands for driving for STEP_S seconds
            driven = min(distance, driven + speed * STEP_S)
            feedback = DriveToGoal.Feedback()
            feedback.distance_remaining_m = distance - driven
            goal_handle.publish_feedback(feedback)
        goal_handle.succeed()
        self.get_logger().info(f'Arrived after {driven} m')
        return DriveToGoal.Result(distance_driven_m=driven)


def main(args=None):
    rclpy.init(args=args)
    executor = MultiThreadedExecutor(num_threads=4)
    spin_until_ctrl_c(DriveServer(), executor)


def single(args=None):
    rclpy.init(args=args)
    spin_until_ctrl_c(DriveServer(), SingleThreadedExecutor())
