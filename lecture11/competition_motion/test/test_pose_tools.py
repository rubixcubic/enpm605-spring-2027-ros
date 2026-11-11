"""Check the quaternion and angle helpers of Lecture 11."""

import math

from competition_motion.pose_tools import (quaternion_from_yaw, wrap_angle,
                                           yaw_from_quaternion)
from geometry_msgs.msg import Quaternion
import pytest


@pytest.mark.parametrize('degrees', [0, 30, 90, 179, -90, -179])
def test_yaw_round_trip(degrees):
    x, y, z, w = quaternion_from_yaw(math.radians(degrees))
    yaw = yaw_from_quaternion(Quaternion(x=x, y=y, z=z, w=w))
    assert math.degrees(yaw) == pytest.approx(degrees)


def test_unit_length():
    q = quaternion_from_yaw(math.radians(30))
    assert math.hypot(*q) == pytest.approx(1.0)


def test_minus_q_is_the_same_turn():
    x, y, z, w = quaternion_from_yaw(math.radians(90))
    minus = Quaternion(x=-x, y=-y, z=-z, w=-w)
    assert math.degrees(yaw_from_quaternion(minus)) == pytest.approx(90)


@pytest.mark.parametrize('degrees, wrapped', [(0, 0), (190, -170),
                                              (-340, 20), (360, 0)])
def test_wrap_angle(degrees, wrapped):
    got = math.degrees(wrap_angle(math.radians(degrees)))
    assert got == pytest.approx(wrapped)
