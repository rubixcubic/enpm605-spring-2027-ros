"""Publish RobotStatus messages with wrong battery_pct values (Lecture 10).

Run with python3 after sourcing the workspace, once as it is and once
with ROS_PYTHON_CHECK_FIELDS=1. Each value is tried in a fresh message.
"""

import time

from competition_interfaces.msg import RobotStatus
import rclpy

rclpy.init()
node = rclpy.create_node('field_checks')
publisher = node.create_publisher(RobotStatus, 'status', 10)
time.sleep(2.0)  # Time for a subscriber to connect (chosen)
for value in [30, 300, '30']:
    msg = RobotStatus(name='scout')
    try:
        msg.battery_pct = value
        publisher.publish(msg)
        print(f'{value!r}: published', flush=True)
    except AssertionError as error:
        print(f'{value!r}: AssertionError: {error}', flush=True)
    time.sleep(0.3)
