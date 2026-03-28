import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

INPUT = Path(__file__).parent / "input.txt"
INITIAL_DIAL = 50


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Rotation:
    direction: Direction
    distance: int

    @classmethod
    def parse(cls, rotation_string: str) -> Rotation:
        return cls(
            direction=Direction(rotation_string[0]), distance=int(rotation_string[1:])
        )

    def perform(self, dial: int) -> int:
        multiplier = -1 if self.direction == Direction.LEFT else 1
        return (dial + multiplier * self.distance) % 100


def read_input(path: Path = INPUT) -> list[Rotation]:
    with open(path) as file:
        return [Rotation.parse(line.strip()) for line in file]


def solve_part1(puzzle_input: list[Rotation]) -> int:
    zeroes = 0
    dial = INITIAL_DIAL

    for rotation in puzzle_input:
        dial = rotation.perform(dial)

        if dial == 0:
            zeroes += 1

    return zeroes


def main():
    logging.basicConfig(level=logging.INFO)

    puzzle_input = read_input()
    answer = solve_part1(puzzle_input)
    logger.info(f"The answer is: {answer}")


if __name__ == "__main__":
    main()
