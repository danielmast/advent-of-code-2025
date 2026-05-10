import logging
import math
import sys
from dataclasses import dataclass
from functools import cache

from day.day import Day

logger = logging.getLogger(__name__)


@dataclass
class JunctionBox:
    x: int
    y: int
    z: int

    def to_list(self) -> list[int]:
        return [self.x, self.y, self.z]

    @cache
    def distance(self, other: JunctionBox) -> float:
        return math.dist(self.to_list(), other.to_list())

    @classmethod
    def parse(cls, junction_box_string: str) -> JunctionBox:
        x, y, z = [int(i) for i in junction_box_string.split(",")]
        return cls(x=x, y=y, z=z)

    def __str__(self):
        return str(self.to_list())

    def __key(self):
        return self.x, self.y, self.z

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, JunctionBox):
            return NotImplemented
        return self.__key == other.__key()


@dataclass(frozen=True)
class Distance:
    box1: JunctionBox
    box2: JunctionBox

    @cache
    def distance(self) -> float:
        return self.box1.distance(self.box2)

    def __str__(self):
        return f"{self.box1} -> {self.box2} = {self.distance()}"

    def __lt__(self, other: Distance) -> bool:
        return self.distance() < other.distance()


class Day8(Day[list[JunctionBox], int, int]):
    def read_input(self) -> list[JunctionBox]:
        with open(self.input_path) as file:
            return [JunctionBox.parse(line.strip()) for line in file]

    def circuit_lookup(self) -> dict[JunctionBox, set[JunctionBox]]:
        lookup = {}
        for box in self.puzzle_input:
            lookup[box] = {box}
        return lookup

    def sorted_distances(self) -> list[Distance]:
        distances = []
        for i, box_i in enumerate(self.puzzle_input):
            for box_j in self.puzzle_input[i + 1 :]:
                distances.append(Distance(box_i, box_j))
        distances.sort()
        return distances

    def connection_count(self):
        """
        Distinguish the number of connections that should be made
        between the example input and the actual input
        """
        if len(self.puzzle_input) == 20:
            return 10
        return 1000

    def merge_circuits(self, limit: int) -> list[set[JunctionBox]] | int:
        distances = self.sorted_distances()
        lookup = self.circuit_lookup()

        for i in range(limit):
            merged = self.merge_circuits_inner(distances[i], lookup)

            # Part 2
            if len(merged) == len(self.puzzle_input):
                return distances[i].box1.x * distances[i].box2.x

        # Part 1
        return [set(s) for s in set(frozenset(s) for s in lookup.values())]

    def merge_circuits_inner(self, distance, lookup) -> set[JunctionBox]:
        merged = lookup[distance.box1].union(lookup[distance.box2])
        self.update_lookup(lookup, merged)
        return merged

    @staticmethod
    def update_lookup(lookup, merged):
        for box in merged:
            lookup[box] = merged

    def solve_part1(self) -> int:
        limit = self.connection_count()
        circuits = self.merge_circuits(limit)
        largest_circuits = sorted(circuits, key=len, reverse=True)[:3]
        multiplied_sizes = math.prod(len(circuit) for circuit in largest_circuits)
        return multiplied_sizes

    def solve_part2(self) -> int:
        limit = sys.maxsize
        return self.merge_circuits(limit)


def main():
    day = Day8()
    day.run()


if __name__ == "__main__":
    main()
