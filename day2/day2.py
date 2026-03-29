import logging
from dataclasses import dataclass
from typing import Iterable

from day.day import Day

logger = logging.getLogger(__name__)


@dataclass
class IDRange:
    start: int
    end: int

    @classmethod
    def parse(cls, s: str) -> IDRange:
        start, end = s.split("-")
        return cls(int(start), int(end))

    def invalid_ids(self, use_divisor_range: bool) -> Iterable[int]:
        return (
            product_id
            for product_id in range(self.start, self.end + 1)
            if not self._is_valid_id(product_id, use_divisor_range)
        )

    @staticmethod
    def _is_valid_id(product_id: int, use_divisor_range: bool) -> bool:
        product_id_str = str(product_id)
        divisor_range = range(2, len(product_id_str) + 1) if use_divisor_range else [2]

        for divisor in divisor_range:
            if len(product_id_str) % divisor != 0:
                continue

            part_len = len(product_id_str) // divisor
            part = product_id_str[:part_len]

            if product_id_str.count(part) == divisor:
                return False

        return True


class Day2(Day[list[IDRange], int, int]):
    def read_input(self) -> list[IDRange]:
        with open(self.input_path) as file:
            return [
                IDRange.parse(range_string)
                for range_string in file.read().strip().split(",")
            ]

    def solve_part1(self) -> int:
        return sum(
            product_id
            for id_range in self.puzzle_input
            for product_id in id_range.invalid_ids(False)
        )

    def solve_part2(self) -> int:
        return sum(
            product_id
            for id_range in self.puzzle_input
            for product_id in id_range.invalid_ids(True)
        )


def main():
    day = Day2()
    day.run()


if __name__ == "__main__":
    main()
