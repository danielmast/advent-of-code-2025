from dataclasses import dataclass
from functools import cache

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
        for y in range(len(self.rows)):
            for x in range(len(self.rows[y])):
                if self.rows[y][x] == "S":
                    return Position(x, y)
        raise ValueError("Start not found")

    def get(self, position: Position) -> str:
        return self.rows[position.y][position.x]


class Node:
    is_splitter: bool | None
    children: set[Node]

    def __init__(self) -> None:
        self.is_splitter = None
        self.children = set()

    def set_is_splitter(self, is_splitter: bool) -> None:
        self.is_splitter = is_splitter

    def add_child(self, child: Node) -> None:
        self.children.add(child)

    @cache
    def total_paths(self) -> int:
        if not self.children:
            return 1
        return sum(c.total_paths() for c in self.children)

    @cache
    def splitters(self) -> set[Node]:
        result = {node for child in self.children for node in child.splitters()}
        if self.is_splitter:
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

            try:
                below_position = head.below()
                below_symbol = grid.get(below_position)

                if below_symbol == "^":
                    node.set_is_splitter(True)
                    new_heads = {below_position.left(), below_position.right()}
                else:
                    node.set_is_splitter(False)
                    new_heads = {below_position}

                for new_head in new_heads:
                    if new_head in nodes:
                        new_node = nodes[new_head]
                    else:
                        new_node = Node()
                        nodes[new_head] = new_node
                        heads.add(new_head)

                    node.add_child(new_node)
            except IndexError:
                pass

            heads.remove(head)

        return DAG(start_node)

    def total_paths(self) -> int:
        return self.start.total_paths()

    def num_splitters(self) -> int:
        return len(self.start.splitters())


class Day7(Day):
    def read_input(self) -> DAG:
        with open(self.input_path) as file:
            lines = [line.rstrip("\n") for line in file]
        return DAG.from_grid(Grid(lines))

    def solve_part1(self) -> int:
        return self.puzzle_input.num_splitters()

    def solve_part2(self) -> int:
        return self.puzzle_input.total_paths()


def main():
    day = Day7()
    day.run()


if __name__ == "__main__":
    main()
