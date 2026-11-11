"""Look up where one frame is in another, once per second (Lecture 11)."""

import math

from competition_motion.pose_tools import yaw_from_quaternion
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from rclpy.time import Time
from tf2_ros import Buffer, TransformException, TransformListener


class FrameListener(Node):
    """Logs the pose of the frame source in the frame target."""

    def __init__(self):
        super().__init__('frame_listener')
        self.declare_parameter('target', 'base_footprint')
        self.declare_parameter('source', 'goal')
        self._buffer = Buffer()  # Keeps the transforms it receives
        self._listener = TransformListener(self._buffer, self)
        self._timer = self.create_timer(1.0, self._look_up)

    def _look_up(self):
        target = self.get_parameter('target').value
        source = self.get_parameter('source').value
        try:
            t = self._buffer.lookup_transform(target, source, Time())
        except TransformException as error:
            self.get_logger().warning(f'No transform: {error}')
            return
        p = t.transform.translation
        yaw = math.degrees(yaw_from_quaternion(t.transform.rotation))
        self.get_logger().info(  # m, m, degrees
            f'{source} in {target}: x={p.x:.2f} y={p.y:.2f} yaw={yaw:.1f}')


def main(args=None):
    rclpy.init(args=args)
    node = FrameListener()
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
