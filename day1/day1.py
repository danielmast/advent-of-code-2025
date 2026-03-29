import logging
from dataclasses import dataclass
from enum import Enum

from day.day import Day

logger = logging.getLogger(__name__)

INITIAL_DIAL = 50


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Rotation:
    direction: Direction
    distance: int

    def __str__(self) -> str:
        return f"{self.direction.value}{self.distance}"

    @classmethod
    def parse(cls, rotation_string: str) -> Rotation:
        return cls(
            direction=Direction(rotation_string[0]), distance=int(rotation_string[1:])
        )

    def _multiplier(self) -> int:
        return -1 if self.direction == Direction.LEFT else 1

    def perform(self, dial: int) -> int:
        return (dial + self._multiplier() * self.distance) % 100

    def zero_crossings(self, dial: int) -> int:
        passed = abs((dial + self._multiplier() * self.distance) // 100)

        if self.perform(dial) == 0 and self.direction == Direction.LEFT:
            passed += 1
        elif dial == 0 and self.direction == Direction.LEFT:
            passed -= 1

        return passed


class Day1(Day[list[Rotation], int, int]):
    def read_input(self) -> list[Rotation]:
        with open(self.input_path) as file:
            return [Rotation.parse(line.strip()) for line in file]

    def solve_part1(self) -> int:
        zeroes = 0
        dial = INITIAL_DIAL

        for rotation in self.puzzle_input:
            dial = rotation.perform(dial)

            if dial == 0:
                zeroes += 1

        return zeroes

    def solve_part2(self) -> int:
        zeroes = 0
        dial = INITIAL_DIAL

        logger.debug(f"Initial dial: {dial}")

        for rotation in self.puzzle_input:
            seen_zero = rotation.zero_crossings(dial)
            zeroes += seen_zero
            dial = rotation.perform(dial)

            logger.debug(f"Rotation: {rotation}, Seen zero: {seen_zero}, dial: {dial}")

        return zeroes


def main():
    day = Day1()
    day.run()


if __name__ == "__main__":
    main()
