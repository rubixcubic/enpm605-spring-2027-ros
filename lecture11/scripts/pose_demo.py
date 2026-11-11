"""Quaternions for a robot that turns about z (Lecture 11, run by path)."""

import math

from competition_motion.pose_tools import (quaternion_from_yaw, wrap_angle,
                                           yaw_from_quaternion)
from geometry_msgs.msg import Quaternion

print('yaw (deg)       x      y      z      w')
for degrees in (0, 30, 90, 180, -90):
    q = quaternion_from_yaw(math.radians(degrees))
    print(f'{degrees:9}' + ''.join(f'{v:7.3f}' for v in q))

x, y, z, w = quaternion_from_yaw(math.radians(30))
print('length:', round(math.sqrt(x * x + y * y + z * z + w * w), 6))
msg = Quaternion(x=x, y=y, z=z, w=w)
print('back to yaw:', round(math.degrees(yaw_from_quaternion(msg)), 6))
minus = Quaternion(x=-x, y=-y, z=-z, w=-w)
print('-q gives yaw:', round(math.degrees(yaw_from_quaternion(minus)), 6))
print('Quaternion():', Quaternion())
print('wrap 190 deg:', round(math.degrees(wrap_angle(math.radians(190))), 6))
