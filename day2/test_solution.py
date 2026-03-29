from pathlib import Path

import pytest

from day2.solution import read_input, solve_part1, solve_part2, INPUT, IDRange

EXAMPLE_INPUT = Path(__file__).parent / "example_input.txt"


@pytest.mark.parametrize(
    "range_string, expected",
    [
        ("92916254-92945956", IDRange(92916254, 92945956)),
        ("5454498003-5454580069", IDRange(5454498003, 5454580069)),
    ],
)
def test_parse_rotation(range_string, expected):
    assert IDRange.parse(range_string) == expected


@pytest.mark.parametrize(
    "product_id, use_divisor_range, expected",
    [
        (11, False, False),
        (11, True, False),
        (95, False, True),
        (1212, False, False),
        (1698528, False, True),
        (824824824, False, True),
        (824824824, True, False),
        (1188511885, False, False),
    ],
)
def test_is_valid_id(product_id, use_divisor_range, expected):
    assert IDRange._is_valid_id(product_id, use_divisor_range) == expected


@pytest.mark.parametrize(
    "id_range, use_divisor_range, expected",
    [
        (IDRange(11, 22), False, {11, 22}),
        (IDRange(11, 22), True, {11, 22}),
        (IDRange(998, 1012), False, {1010}),
        (IDRange(998, 1012), True, {999, 1010}),
        (IDRange(1188511880, 1188511890), False, {1188511885}),
        (IDRange(1698522, 1698528), False, set()),
    ],
)
def test_invalid_ids(id_range, use_divisor_range, expected):
    assert set(id_range.invalid_ids(use_divisor_range)) == expected


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (EXAMPLE_INPUT, 1227775554),
        (INPUT, 23039913998),
    ],
)
def test_solve_part1(input_path, expected):
    puzzle_input = read_input(input_path)
    assert solve_part1(puzzle_input) == expected


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (EXAMPLE_INPUT, 4174379265),
        (INPUT, 35950619148),
    ],
)
def test_solve_part2(input_path, expected):
    puzzle_input = read_input(input_path)
    assert solve_part2(puzzle_input) == expected
