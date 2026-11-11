"""Build a QoS profile from three parameters of a node (Lecture 10)."""

from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy

RELIABILITY = {'reliable': ReliabilityPolicy.RELIABLE,
               'best_effort': ReliabilityPolicy.BEST_EFFORT}
DURABILITY = {'volatile': DurabilityPolicy.VOLATILE,
              'transient_local': DurabilityPolicy.TRANSIENT_LOCAL}


def declare_qos(node):
    """Declare reliability, durability and depth; return the profile."""
    node.declare_parameter('reliability', 'reliable')  # The defaults
    node.declare_parameter('durability', 'volatile')
    node.declare_parameter('depth', 10)
    depth = node.get_parameter('depth').value
    reliability = node.get_parameter('reliability').value
    durability = node.get_parameter('durability').value
    return QoSProfile(depth=depth,  # History: keep last, the default
                      reliability=RELIABILITY[reliability],
                      durability=DURABILITY[durability])
