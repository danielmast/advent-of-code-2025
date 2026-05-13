import logging
from dataclasses import dataclass
from itertools import product

from day.day import Day, PuzzleInput

logger = logging.getLogger(__name__)


@dataclass
class Tile:
    x: int
    y: int

    @classmethod
    def from_str(cls, s: str) -> "Tile":
        x, y = s.strip().split(",")
        return cls(int(x), int(y))

    def area(self, other: Tile) -> int:
        return abs(self.x - other.x + 1) * abs(self.y - other.y + 1)


class Day9(Day[list[Tile], int, int]):
    def read_input(self) -> PuzzleInput:
        with open(self.input_path) as file:
            return [Tile.from_str(line) for line in file.readlines()]

    def solve_part1(self) -> int:
        tile_pairs = list(product(self.puzzle_input, self.puzzle_input))
        pair_with_max_area = max(tile_pairs, key=lambda pair: pair[0].area(pair[1]))
        return pair_with_max_area[0].area(pair_with_max_area[1])

    def solve_part2(self) -> int:
        raise NotImplementedError


def main():
    day = Day9()
    day.run()


if __name__ == "__main__":
    main()
