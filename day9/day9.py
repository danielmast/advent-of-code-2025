import logging
import sys
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import cache
from itertools import product

from day.day import Day, PuzzleInput

logger = logging.getLogger(__name__)

SHOULD_DRAW = False
sys.setrecursionlimit(100000)


class Color(Enum):
    RED = "R"
    GREEN = "G"
    OTHER = "."


@dataclass
class Point:
    x: int
    y: int

    def neighbours(self) -> list[Point]:
        return [
            Point(self.x - 1, self.y),
            Point(self.x + 1, self.y),
            Point(self.x, self.y - 1),
            Point(self.x, self.y + 1),
        ]

    def in_dimensions(self, d: tuple[int, int, int, int]) -> bool:
        return d[0] <= self.x <= d[1] and d[2] <= self.y <= d[3]


@dataclass
class Tile:
    x: int
    y: int
    color: Color

    @classmethod
    def from_str(cls, s: str) -> "Tile":
        x, y = s.strip().split(",")
        return cls(int(x), int(y), Color.RED)

    def area(self, other: Tile) -> int:
        return abs(self.x - other.x + 1) * abs(self.y - other.y + 1)


class ColorMap:
    map: defaultdict[int, defaultdict[int, Color]]
    red_tiles: list[Tile]

    def __init__(self, red_tiles) -> None:
        self.red_tiles = red_tiles
        self.map = defaultdict(lambda: defaultdict(lambda: Color.OTHER))
        self.draw()
        self.add_red()
        self.draw()
        self.add_green()

    @cache
    def dimensions(self) -> tuple[int, int, int, int]:
        x_min = min(tile.x for tile in self.red_tiles)
        x_max = max(tile.x for tile in self.red_tiles)
        y_min = min(tile.y for tile in self.red_tiles)
        y_max = max(tile.y for tile in self.red_tiles)
        return x_min, x_max, y_min, y_max

    def add_red(self):
        for tile in self.red_tiles:
            self.map[tile.x][tile.y] = Color.RED

    def add_green(self):
        self.add_green_between_adjacent_tiles()
        self.draw()
        self.make_green_and_spread(self.find_start())
        self.draw()

    def add_green_between_adjacent_tiles(self):
        for i in range(0, len(self.red_tiles)):
            tile1 = self.red_tiles[i]
            tile2 = self.red_tiles[(i + 1) % len(self.red_tiles)]
            self.add_green_between_pair(tile1, tile2)

    def add_green_between_pair(self, tile1: Tile, tile2: Tile):
        if tile1.x == tile2.x:
            min_y = min(tile1.y, tile2.y)
            max_y = max(tile1.y, tile2.y)
            for y in range(min_y + 1, max_y):
                self.map[tile1.x][y] = Color.GREEN
        else:
            min_x = min(tile1.x, tile2.x)
            max_x = max(tile1.x, tile2.x)
            for x in range(min_x + 1, max_x):
                self.map[x][tile1.y] = Color.GREEN

    def find_start(self) -> Point:
        if len(self.red_tiles) == 8:  # example input
            return Point(x=8, y=2)
        return Point(x=97580, y=51497)  # real input

    def make_green_and_spread(self, point: Point):
        assert point.in_dimensions(self.dimensions())

        if self.map[point.x][point.y] == Color.OTHER:
            self.map[point.x][point.y] = Color.GREEN
            for neighbour in point.neighbours():
                self.make_green_and_spread(neighbour)

    def draw(self):
        if not SHOULD_DRAW:
            return

        x_min, x_max, y_min, y_max = self.dimensions()
        for y in range(y_max + 1):
            row = ""
            for x in range(x_max + 1):
                color = self.map[x][y]
                row += color.value
            print(row)
        print()


class Day9(Day[list[Tile], int, int]):
    def read_input(self) -> PuzzleInput:
        with open(self.input_path) as file:
            return [Tile.from_str(line) for line in file.readlines()]

    def red_tile_pairs(self) -> list[tuple[Tile, Tile]]:
        return list(product(self.puzzle_input, self.puzzle_input))

    def solve_part1(self) -> int:
        tile_pairs = self.red_tile_pairs()
        pair_with_max_area = max(tile_pairs, key=lambda pair: pair[0].area(pair[1]))
        return pair_with_max_area[0].area(pair_with_max_area[1])

    def solve_part2(self) -> int:
        """
        1. Construct a map: for every tile: red, green or other
        2. Sort tile_pairs on area DESC
        3. Iterate, for every pair, check if valid (based on map) by scanning

        """
        map = ColorMap(self.puzzle_input)

        largest_valid_pair = self.find_largest_valid_pair(map)

        return largest_valid_pair[0].area(largest_valid_pair[1])

    def find_largest_valid_pair(self, map) -> tuple[Tile, Tile]:
        tile_pairs = self.red_tile_pairs()
        tile_pairs.sort(key=lambda pair: pair[0].area(pair[1]), reverse=True)

        for tile1, tile2 in tile_pairs:
            if self.is_valid_pair(tile1, tile2, map):
                return tile1, tile2

        raise AssertionError

    @staticmethod
    def is_valid_pair(tile1: Tile, tile2: Tile, map: ColorMap) -> bool:
        x_min = min(tile1.x, tile2.x)
        x_max = max(tile1.x, tile2.x)
        y_min = min(tile1.y, tile2.y)
        y_max = max(tile1.y, tile2.y)

        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                if map.map[x][y] == Color.OTHER:
                    return False

        return True


def main():
    day = Day9()
    day.run()


if __name__ == "__main__":
    main()
