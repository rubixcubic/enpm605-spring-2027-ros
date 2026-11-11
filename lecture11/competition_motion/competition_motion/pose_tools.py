"""Quaternions and angles for a robot that turns only about z (Lecture 11)."""

import math


def quaternion_from_yaw(yaw):
    """Return (x, y, z, w), w last, for a turn of yaw radians about z."""
    return (0.0, 0.0, math.sin(yaw / 2), math.cos(yaw / 2))


def yaw_from_quaternion(q):
    """Return the yaw, in radians, of a geometry_msgs Quaternion."""
    return math.atan2(2 * (q.w * q.z + q.x * q.y),
                      1 - 2 * (q.y * q.y + q.z * q.z))


def wrap_angle(angle):
    """Return the same angle, in radians, between -pi and pi."""
    return (angle + math.pi) % (2 * math.pi) - math.pi
