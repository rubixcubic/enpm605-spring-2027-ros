"""Tests of grid_math: cells, points, and inflation costs (Lecture 12)."""

import math

from competition_nav.grid_math import (cell_to_point, inflation_cost,
                                       INSCRIBED, LETHAL, point_to_cell)
import pytest

ORIGIN = (-1.0, -2.0)  # A map's origin, m (chosen for the tests)


def test_cell_zero_is_next_to_the_origin():
    assert cell_to_point(0, 0, ORIGIN, 0.05) == pytest.approx((-0.975, -1.975))


def test_cell_to_point_moves_one_resolution_per_cell():
    x, y = cell_to_point(10, 4, ORIGIN, 0.05)
    assert (x, y) == pytest.approx((-1.0 + 10.5 * 0.05, -2.0 + 4.5 * 0.05))


def test_point_to_cell_inverts_cell_to_point():
    for col, row in [(0, 0), (3, 7), (120, 85)]:
        x, y = cell_to_point(col, row, ORIGIN, 0.05)
        assert point_to_cell(x, y, ORIGIN, 0.05) == (col, row)


def test_point_left_of_the_origin_has_a_negative_column():
    assert point_to_cell(-1.01, -1.99, ORIGIN, 0.05) == (-1, 0)


def test_cost_on_an_obstacle_is_lethal():
    assert inflation_cost(0.0, 0.22, 3.0, 0.7) == LETHAL


def test_cost_inside_the_robot_radius_is_inscribed():
    assert inflation_cost(0.20, 0.22, 3.0, 0.7) == INSCRIBED


def test_cost_falls_off_exponentially():
    expected = int(252 * math.exp(-3.0 * (0.40 - 0.22)))
    assert inflation_cost(0.40, 0.22, 3.0, 0.7) == expected == 146


def test_cost_beyond_the_inflation_radius_is_zero():
    assert inflation_cost(0.75, 0.22, 3.0, 0.7) == 0
