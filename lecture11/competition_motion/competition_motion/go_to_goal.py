"""Drive to a goal with a proportional controller, from /odom (Lecture 11)."""

import math

from competition_motion.pose_tools import wrap_angle, yaw_from_quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

PERIOD_S = 0.1  # The control loop runs at 10 Hz (chosen)
MAX_V_MPS = 0.3  # Under the Waffle's 0.46 m/s (chosen)
MAX_W_RPS = 1.0  # Under the Waffle's 1.9 rad/s (chosen)
TURN_FIRST_RAD = math.radians(45)  # Turn in place above this (chosen)


def clamp(value, limit):
    """Return value, kept between -limit and limit."""
    return max(-limit, min(limit, value))


class GoToGoal(Node):
    """Turns toward the goal and drives to it, then stops."""

    def __init__(self, name='go_to_goal'):
        super().__init__(name)
        self.declare_parameter('goal_x', 2.0)  # In odom, m (chosen)
        self.declare_parameter('goal_y', 1.0)
        self.declare_parameter('k_rho', 0.5)  # Gain on distance, 1/s
        self.declare_parameter('k_alpha', 1.5)  # Gain on heading, 1/s
        self.declare_parameter('tolerance_m', 0.05)
        self._pose = None  # (x, y, yaw) in odom, from the last message
        self._ticks = 0
        self._done = False
        self._cmd = self.create_publisher(Twist, 'cmd_vel', 10)
        self._odom = self.create_subscription(
            Odometry, 'odom', self._on_odom, 10)
        self._timer = self.create_timer(PERIOD_S, self._control)

    def _on_odom(self, msg):
        p = msg.pose.pose
        self._pose = (p.position.x, p.position.y,
                      yaw_from_quaternion(p.orientation))

    def errors(self):
        """Return (distance, heading error) to the goal, or None."""
        if self._pose is None:
            return None
        x, y, yaw = self._pose
        dx = self.get_parameter('goal_x').value - x
        dy = self.get_parameter('goal_y').value - y
        return math.hypot(dx, dy), wrap_angle(math.atan2(dy, dx) - yaw)

    def _control(self):
        e = None if self._done else self.errors()
        if e is None:
            return
        rho, alpha = e
        cmd = Twist()  # All zeros: stop
        if rho < self.get_parameter('tolerance_m').value:
            self._done = True
            self._cmd.publish(cmd)
            x, y = self._pose[:2] if self._pose else (math.nan, math.nan)
            self.get_logger().info(
                f'Arrived at t={self._ticks * PERIOD_S:.1f} s: '
                f'x={x:.2f} y={y:.2f} rho={rho:.3f}')
            return
        k_rho = self.get_parameter('k_rho').value
        k_alpha = self.get_parameter('k_alpha').value
        if abs(alpha) < TURN_FIRST_RAD:
            cmd.linear.x = clamp(k_rho * rho, MAX_V_MPS)
        cmd.angular.z = clamp(k_alpha * alpha, MAX_W_RPS)
        self._cmd.publish(cmd)
        if self._ticks % 10 == 0:  # Once per second of ticks (wall clock)
            self.get_logger().info(  # s, m, degrees, m/s, rad/s
                f't={self._ticks * PERIOD_S:.1f} rho={rho:.2f} '
                f'alpha={math.degrees(alpha):.1f} '
                f'v={cmd.linear.x:.2f} w={cmd.angular.z:.2f}')
        self._ticks += 1


def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
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
