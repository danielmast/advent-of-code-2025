from pathlib import Path

import pytest

from day1.solution import (
    Direction,
    Rotation,
    read_input,
    solve_part1,
    solve_part2,
    INPUT,
)

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


@pytest.mark.parametrize(
    "dial, rotation, expected",
    [
        (10, Rotation(Direction.RIGHT, 20), 0),
        (80, Rotation(Direction.RIGHT, 20), 1),
        (90, Rotation(Direction.RIGHT, 20), 1),
        (90, Rotation(Direction.RIGHT, 250), 3),
        (90, Rotation(Direction.RIGHT, 310), 4),
        (0, Rotation(Direction.LEFT, 20), 0),
        (10, Rotation(Direction.LEFT, 20), 1),
        (20, Rotation(Direction.LEFT, 20), 1),
        (90, Rotation(Direction.LEFT, 20), 0),
        (90, Rotation(Direction.LEFT, 250), 2),
        (90, Rotation(Direction.LEFT, 290), 3),
    ],
)
def test_zero_crossings(dial, rotation, expected):
    assert rotation.zero_crossings(dial) == expected


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (EXAMPLE_INPUT, 3),
        (INPUT, 1177),
    ],
)
def test_solve_part1(input_path, expected):
    puzzle_input = read_input(input_path)
    assert solve_part1(puzzle_input) == expected


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (EXAMPLE_INPUT, 6),
        (INPUT, 6768),
    ],
)
def test_solve_part2(input_path, expected):
    puzzle_input = read_input(input_path)
    assert solve_part2(puzzle_input) == expected
