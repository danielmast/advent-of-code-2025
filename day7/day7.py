from dataclasses import dataclass
from functools import cached_property

from day.day import Day


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def below(self) -> Position:
        return Position(self.x, self.y + 1)

    def left(self) -> Position:
        return Position(self.x - 1, self.y)

    def right(self) -> Position:
        return Position(self.x + 1, self.y)


@dataclass
class Grid:
    rows: list[str]

    def get_start_position(self) -> Position:
        for y, row in enumerate(self.rows):
            for x, char in enumerate(row):
                if char == "S":
                    return Position(x, y)
        raise ValueError("Start not found")

    def __getitem__(self, position: Position) -> str:
        return self.rows[position.y][position.x]

    def contains(self, position: Position) -> bool:
        return 0 <= position.y < len(self.rows) and 0 <= position.x < len(
            self.rows[position.y]
        )


class Node:
    def __init__(self) -> None:
        self.children: set[Node] = set()

    @cached_property
    def total_paths(self) -> int:
        if not self.children:
            return 1
        return sum(c.total_paths for c in self.children)

    @cached_property
    def splitters(self) -> set[Node]:
        result = {node for child in self.children for node in child.splitters}

        if len(self.children) == 2:
            result.add(self)

        return result


@dataclass
class DAG:
    start: Node

    @classmethod
    def from_grid(cls, grid: Grid) -> DAG:
        start_position = grid.get_start_position()
        start_node = Node()

        nodes: dict[Position, Node] = {start_position: start_node}
        heads = {start_position}

        while heads:
            head = next(iter(heads))
            node = nodes[head]

            below_position = head.below()

            if grid.contains(below_position):
                if grid[below_position] == "^":
                    new_heads = {below_position.left(), below_position.right()}
                else:
                    new_heads = {below_position}

                for new_head in new_heads:
                    if new_head in nodes:
                        new_node = nodes[new_head]
                    else:
                        new_node = Node()
                        nodes[new_head] = new_node
                        heads.add(new_head)

                    node.children.add(new_node)

            heads.remove(head)

        return DAG(start_node)

    def total_paths(self) -> int:
        return self.start.total_paths

    def splitters(self) -> set[Node]:
        return self.start.splitters


class Day7(Day):
    def read_input(self) -> DAG:
        with open(self.input_path) as file:
            lines = [line.rstrip("\n") for line in file]
        return DAG.from_grid(Grid(lines))

    def solve_part1(self) -> int:
        return len(self.puzzle_input.splitters())

    def solve_part2(self) -> int:
        return self.puzzle_input.total_paths()


def main():
    day = Day7()
    day.run()


if __name__ == "__main__":
    main()
