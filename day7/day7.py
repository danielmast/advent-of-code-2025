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
    children: set[Node]

    def __init__(self):
        self.children = set()

    def add_child(self, child: Node) -> None:
        self.children.add(child)

    @cache
    def total_paths(self) -> int:
        if not self.children:
            return 1
        return sum(c.total_paths() for c in self.children)


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
            head = list(heads)[0]
            node = nodes[head]

            try:
                below_position = head.below()
                below_symbol = grid.get(below_position)

                if below_symbol == "^":
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

                    node.add_child(new_node)
            except IndexError:
                pass

            heads.remove(head)

        return DAG(start_node)

    def total_paths(self) -> int:
        return self.start.total_paths()


class Day7(Day):
    def read_input(self) -> Grid:
        with open(self.input_path) as file:
            lines = [line.rstrip("\n") for line in file]
        return Grid(lines)

    def solve_part1(self) -> int:
        splits = set()
        heads = {self.puzzle_input.get_start_position()}

        while heads:
            head = list(heads)[0]

            try:
                below_position = head.below()
                below_symbol = self.puzzle_input.get(below_position)

                if below_symbol == "^":
                    splits.add(below_position)
                    heads.add(below_position.left())
                    heads.add(below_position.right())
                else:
                    heads.add(below_position)
            except IndexError:
                pass

            heads.remove(head)

        return len(splits)

    def solve_part2(self) -> int:
        dag = DAG.from_grid(self.puzzle_input)
        return dag.total_paths()


def main():
    day = Day7()
    day.run()


if __name__ == "__main__":
    main()
