import pytest

from day.day_test import DayTest
from day3.day3 import Day3, Bank


class TestDay3(DayTest):
    day_class = Day3
    example_answer_part1 = 357
    example_answer_part2 = 3121910778619
    answer_part1 = 17332
    answer_part2 = 172516781546707

    @pytest.mark.parametrize(
        "bank, length, expected",
        [
            (Bank("987654321111111"), 2, 98),
            (Bank("987654321111111"), 12, 987654321111),
            (Bank("234234234234278"), 2, 78),
            (Bank("234234234234278"), 12, 434234234278),
            (Bank("818181911112111"), 2, 92),
            (Bank("818181911112111"), 12, 888911112111),
        ],
    )
    def test_largest_joltage(self, bank, length, expected):
        assert bank.largest_joltage(length) == expected
