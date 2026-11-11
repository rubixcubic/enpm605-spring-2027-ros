"""A controller with a slow callback and a fast one (Lecture 9)."""

import time

from rclpy.node import Node

PLAN_PERIOD_S = 1.0  # One plan per second, chosen for this example
CHECK_PERIOD_S = 0.1  # Ten checks per second, chosen for this example


class RobotController(Node):
    """Plans a route every 1.0 s and checks safety every 0.1 s."""

    def __init__(self, plan_s=0.5, plan_group=None, check_group=None):
        super().__init__('robot_controller')
        self._groups = (plan_group, check_group)  # Keep both groups
        self._plan_s = plan_s  # How long one plan takes, in seconds
        self._plans_done = 0
        self._t0 = time.monotonic()
        self._last_check = self._t0
        self._plan_timer = self.create_timer(
            PLAN_PERIOD_S, self._plan, callback_group=plan_group)
        self._check_timer = self.create_timer(
            CHECK_PERIOD_S, self._check_safety,
            callback_group=check_group)

    def _plan(self):
        done = self._plans_done  # Read at the start of the plan
        self._log('plan start')
        time.sleep(self._plan_s)  # Stands for the work of planning a route
        self._plans_done = done + 1  # Written back plan_s seconds later
        self._log(f'plan end, plans done: {self._plans_done}')

    def _check_safety(self):
        now = time.monotonic()
        gap = now - self._last_check
        self._last_check = now
        if gap > 1.5 * CHECK_PERIOD_S:  # Late: over 0.15 s since the last
            self._log(f'check late: {gap:.2f} s since the last')

    def _log(self, text):
        elapsed = time.monotonic() - self._t0
        self.get_logger().info(f'{elapsed:.2f} s: {text}')
