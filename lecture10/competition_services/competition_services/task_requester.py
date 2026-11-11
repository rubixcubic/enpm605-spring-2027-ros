"""A node that sends a task from a timer callback (Lecture 10)."""

from competition_executors.controller_runs import spin_until_ctrl_c
from competition_interfaces.srv import AssignTask
import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
from rclpy.node import Node

TASKS = [('pick widget', 5), ('carry crate', 6), ('scan shelf', 3)]
PERIOD_S = 1.0  # One request per second, chosen for this example


class TaskRequester(Node):
    """Sends the tasks of TASKS, one per timer callback."""

    def __init__(self, wait_in_callback=False, client_group=None):
        super().__init__('task_requester')
        self._wait = wait_in_callback  # True: call(); False: call_async()
        self._client = self.create_client(
            AssignTask, 'assign_task', callback_group=client_group)
        self._tasks = list(TASKS)
        self._timer = self.create_timer(PERIOD_S, self._send_next)

    def _send_next(self):
        if not self._tasks or not self._client.service_is_ready():
            return
        task, minutes = self._tasks.pop(0)
        request = AssignTask.Request(task=task, minutes=minutes)
        self.get_logger().info(f'Sending {task}')
        if self._wait:
            self._log_reply(self._client.call(request))  # Blocks here
        else:
            future = self._client.call_async(request)
            future.add_done_callback(
                lambda done: self._log_reply(done.result()))

    def _log_reply(self, reply):
        self.get_logger().info(
            f'Reply: accepted {reply.accepted}, battery {reply.battery_pct}%')


def async_requester(args=None):
    rclpy.init(args=args)
    spin_until_ctrl_c(TaskRequester(), SingleThreadedExecutor())


def sync_requester(args=None):
    rclpy.init(args=args)
    node = TaskRequester(wait_in_callback=True)  # Timer, client: one group
    spin_until_ctrl_c(node, SingleThreadedExecutor())


def sync_two_groups(args=None):
    rclpy.init(args=args)
    node = TaskRequester(wait_in_callback=True,
                         client_group=MutuallyExclusiveCallbackGroup())
    spin_until_ctrl_c(node, MultiThreadedExecutor(num_threads=2))
