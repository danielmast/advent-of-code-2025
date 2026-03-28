from pathlib import Path

import pytest

from day1.solution import Direction, Rotation, read_input, solve_part1


EXAMPLE_INPUT = Path(__file__).parent / "example_input.txt"


@pytest.mark.parametrize(
    "rotation_string, expected",
    [("R24", Rotation(Direction.RIGHT, 24)), ("L38", Rotation(Direction.LEFT, 38))],
)
def test_parse_rotation(rotation_string, expected):
    assert Rotation.parse(rotation_string) == expected


@pytest.mark.parametrize(
    "dial, rotation, expected",
    [
        (10, Rotation(Direction.RIGHT, 20), 30),
        (80, Rotation(Direction.RIGHT, 20), 0),
        (90, Rotation(Direction.RIGHT, 20), 10),
        (10, Rotation(Direction.LEFT, 20), 90),
        (20, Rotation(Direction.LEFT, 20), 0),
        (90, Rotation(Direction.LEFT, 20), 70),
    ],
)
def test_perform_rotation(dial, rotation, expected):
    assert rotation.perform(dial) == expected


def test_solve_part1():
    puzzle_input = read_input(EXAMPLE_INPUT)
    assert solve_part1(puzzle_input) == 3


def test_solve_part1_regression():
    assert solve_part1(read_input()) == 1177
