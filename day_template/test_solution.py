from pathlib import Path

import pytest

from day_template.solution import read_input, solve_part1, solve_part2, INPUT

EXAMPLE_INPUT = Path(__file__).parent / "example_input.txt"


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (EXAMPLE_INPUT, ...),
        (INPUT, ...),
    ],
)
def test_solve_part1(input_path, expected):
    puzzle_input = read_input(input_path)
    assert solve_part1(puzzle_input) == expected


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (EXAMPLE_INPUT, ...),
        (INPUT, ...),
    ],
)
def test_solve_part2(input_path, expected):
    puzzle_input = read_input(input_path)
    assert solve_part2(puzzle_input) == expected
