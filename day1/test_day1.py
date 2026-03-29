import pytest

from day1.day1 import (
    Direction,
    Rotation,
    Day1,
)
from day.day_test import DayTest


class TestDay1(DayTest):
    day_class = Day1
    example_answer_part1 = 3
    example_answer_part2 = 6
    answer_part1 = 1177
    answer_part2 = 6768

    @pytest.mark.parametrize(
        "rotation_string, expected",
        [("R24", Rotation(Direction.RIGHT, 24)), ("L38", Rotation(Direction.LEFT, 38))],
    )
    def test_parse_rotation(self, rotation_string, expected):
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
    def test_perform_rotation(self, dial, rotation, expected):
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
    def test_zero_crossings(self, dial, rotation, expected):
        assert rotation.zero_crossings(dial) == expected
