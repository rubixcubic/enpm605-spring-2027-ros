"""The go-to-goal controller, with TF2 doing the geometry (Lecture 11)."""

import math

from competition_motion.go_to_goal import GoToGoal
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener


class TfGoToGoal(GoToGoal):
    """Reads where the goal is from TF2, instead of from /odom."""

    def __init__(self):
        super().__init__('tf_go_to_goal')
        self.declare_parameter('goal_frame', 'goal')
        self._buffer = Buffer()
        self._listener = TransformListener(self._buffer, self)

    def errors(self):
        """Return (distance, heading error) to the goal, or None."""
        goal = self.get_parameter('goal_frame').value
        try:
            t = self._buffer.lookup_transform(
                'base_footprint', goal, Time())
        except TransformException:
            return None  # No transform yet: send nothing
        p = t.transform.translation  # The goal, seen from the robot
        return math.hypot(p.x, p.y), math.atan2(p.y, p.x)


def main(args=None):
    rclpy.init(args=args)
    node = TfGoToGoal()
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
