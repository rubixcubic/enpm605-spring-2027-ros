"""One RobotController, run by different executors (Lecture 9)."""

from competition_executors.robot_controller import RobotController
import rclpy
from rclpy.callback_groups import (
    MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup)
from rclpy.executors import (
    ExternalShutdownException, MultiThreadedExecutor, SingleThreadedExecutor)

THREADS = 4  # Threads in the pool, chosen for this example


def spin_until_ctrl_c(node, executor):
    """Run the node's callbacks with the executor until Ctrl+C."""
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    except Exception:  # Ctrl+C can also end spin() with an RCLError
        if rclpy.ok():  # ROS 2 still running: a real error
            raise
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.try_shutdown()


def single_threaded(args=None):
    rclpy.init(args=args)
    node = RobotController()  # Both timers in the default group
    spin_until_ctrl_c(node, SingleThreadedExecutor())


def multi_threaded(args=None):
    rclpy.init(args=args)
    node = RobotController()  # Both timers in the default group
    spin_until_ctrl_c(node, MultiThreadedExecutor(num_threads=THREADS))


def two_groups(args=None):
    rclpy.init(args=args)
    node = RobotController(plan_group=MutuallyExclusiveCallbackGroup(),
                           check_group=MutuallyExclusiveCallbackGroup())
    spin_until_ctrl_c(node, MultiThreadedExecutor(num_threads=THREADS))


def slow_plan(args=None):
    rclpy.init(args=args)
    node = RobotController(plan_s=1.5,  # Longer than its 1.0 s period
                           plan_group=MutuallyExclusiveCallbackGroup(),
                           check_group=MutuallyExclusiveCallbackGroup())
    spin_until_ctrl_c(node, MultiThreadedExecutor(num_threads=THREADS))


def reentrant_plan(args=None):
    rclpy.init(args=args)
    node = RobotController(plan_s=1.5,  # Longer than its 1.0 s period
                           plan_group=ReentrantCallbackGroup(),
                           check_group=MutuallyExclusiveCallbackGroup())
    spin_until_ctrl_c(node, MultiThreadedExecutor(num_threads=THREADS))
