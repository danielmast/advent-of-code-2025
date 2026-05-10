import logging
import math
from dataclasses import dataclass
from functools import cache

from day.day import Day

logger = logging.getLogger(__name__)


@dataclass
class JunctionBox:
    x: int
    y: int
    z: int
    connected: set[JunctionBox]

    def to_list(self) -> list[int]:
        return [self.x, self.y, self.z]

    @cache
    def distance(self, other: JunctionBox) -> float:
        return math.dist(self.to_list(), other.to_list())

    def connect(self, other: JunctionBox) -> None:
        print(f"Connect: {self} <-> {other}")
        self.connected.add(other)
        other.connected.add(self)

    def circuit(self, seen=None) -> set[JunctionBox]:
        if seen is None:
            seen = {self}
        circuit = self.connected.copy()
        circuit.add(self)

        for box in self.connected:
            if box not in seen:
                seen = seen.union({box})
                circuit = circuit.union(box.circuit(seen))

        return circuit

    @classmethod
    def parse(cls, junction_box_string: str) -> JunctionBox:
        x, y, z = [int(i) for i in junction_box_string.split(",")]
        return cls(x=x, y=y, z=z, connected=set())

    def __str__(self):
        return str(self.to_list())

    def __key(self):
        return (self.x, self.y, self.z)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, JunctionBox):
            return NotImplemented
        return self.__key == other.__key()


@dataclass(frozen=True)
class Connection:
    box1: JunctionBox
    box2: JunctionBox

    @cache
    def distance(self) -> float:
        return self.box1.distance(self.box2)

    def __str__(self):
        return f"{self.box1} -> {self.box2} = {self.distance()}"

    def __lt__(self, other: Connection) -> bool:
        return self.distance() < other.distance()


class Day8(Day[list[JunctionBox], int, int]):
    def read_input(self) -> list[JunctionBox]:
        with open(self.input_path) as file:
            return [JunctionBox.parse(line.strip()) for line in file]

    def distances(self) -> list[Connection]:
        distances = []
        for i, box_i in enumerate(self.puzzle_input):
            for box_j in self.puzzle_input[i + 1 :]:
                distances.append(Connection(box_i, box_j))
        return distances

    def get_connection_count(self):
        """
        Distinguish the number of connections that should be made
        between the example input and the actual input
        """
        if len(self.puzzle_input) == 20:
            return 10
        return 1000

    def solve_part1(self) -> int:
        distances = self.distances()
        distances.sort()

        for i in range(self.get_connection_count()):
            distances[i].box1.connect(distances[i].box2)

        circuits = self.circuits()
        largest_circuits = sorted(circuits, key=len, reverse=True)[:3]
        multiplied_sizes = math.prod(len(circuit) for circuit in largest_circuits)

        return multiplied_sizes

    def circuits(self) -> list[set[JunctionBox]]:
        seen_boxes = set()
        circuits = []
        for box in self.puzzle_input:
            if box not in seen_boxes:
                circuit = box.circuit()
                circuits.append(circuit)
                seen_boxes = seen_boxes.union(circuit)

        return circuits

    def solve_part2(self) -> int:
        """
        Like in part 1, also connect, but dont stop at 1000
        Instead, after every connection, check if the circuit length of a random box equals the input size
        Then multiply the Xs of the last connected boxes
        """

        distances = self.distances()
        distances.sort()

        for distance in distances:
            distance.box1.connect(distance.box2)

            circuit = self.puzzle_input[0].circuit()
            if len(circuit) == len(self.puzzle_input):
                return distance.box1.x * distance.box2.x

        raise AssertionError


def main():
    day = Day8()
    day.run()


if __name__ == "__main__":
    main()
