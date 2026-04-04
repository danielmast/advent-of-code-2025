from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from day.day import Day


@dataclass
class Grid:
    grid: list[list[Tile]]
    width: int
    height: int

    @classmethod
    def parse_file(cls, path: Path) -> Grid:
        with open(path) as file:
            grid = [
                [Tile(x, y, char == "@") for x, char in enumerate(line.strip())]
                for y, line in enumerate(file)
            ]
        return cls(grid, len(grid[0]), len(grid))

    def get(self, x, y) -> Tile:
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError
        return self.grid[y][x]

    def tile_iterator(self) -> Iterator[Tile]:
        for row in self.grid:
            for tile in row:
                yield tile


@dataclass
class Tile:
    x: int
    y: int
    is_paper: bool

    def neighbours(self, grid) -> Iterator[Tile]:
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if not (i == self.x and j == self.y):
                    try:
                        yield grid.get(i, j)
                    except IndexError:
                        pass

    def num_paper_neighbours(self, grid: Grid) -> int:
        return sum(1 for n in self.neighbours(grid) if n.is_paper)


class Day4(Day):
    def read_input(self) -> Grid:
        return Grid.parse_file(self.input_path)

    def solve_part1(self) -> int:
        neighbour_limit = 4

        return sum(
            1
            for tile in self.puzzle_input.tile_iterator()
            if tile.is_paper
            and tile.num_paper_neighbours(self.puzzle_input) < neighbour_limit
        )

    def solve_part2(self) -> int:
        pass


def main():
    day = Day4()
    day.run()


if __name__ == "__main__":
    main()
