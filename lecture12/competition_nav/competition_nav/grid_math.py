"""Cells, points, and costs of a 2D grid map (Lecture 12)."""

import math

LETHAL = 254  # Nav2's cost of a cell that holds an obstacle
INSCRIBED = 253  # Nav2's cost of a cell closer than the robot's radius


def cell_to_point(col, row, origin, resolution):
    """Return the (x, y) of the center of cell (col, row), in m."""
    return (origin[0] + (col + 0.5) * resolution,
            origin[1] + (row + 0.5) * resolution)


def point_to_cell(x, y, origin, resolution):
    """Return the (col, row) of the cell that holds the point (x, y)."""
    return (math.floor((x - origin[0]) / resolution),
            math.floor((y - origin[1]) / resolution))


def inflation_cost(distance_m, inscribed_m, scaling, radius_m):
    """Return Nav2's inflation cost at a distance from an obstacle."""
    if distance_m == 0:
        return LETHAL
    if distance_m <= inscribed_m:
        return INSCRIBED
    if distance_m > radius_m:
        return 0
    factor = math.exp(-scaling * (distance_m - inscribed_m))
    return int((INSCRIBED - 1) * factor)
