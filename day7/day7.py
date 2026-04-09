from dataclasses import dataclass

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


class Day7(Day):
    def read_input(self) -> Grid:
        with open(self.input_path) as file:
            lines = [line.rstrip("\n") for line in file]
        return Grid(lines)

    def solve_part1(self) -> int:
        """
        Start at S
        Traverse down
        If a splitter is met, create new heads
        Keep the positions of the heads in a set, so that there are no duplicates

        So basically, iterate over each head (starting with one), and look down.
        if splitter, create 2 new heads. of dot, create 1 new head
        count up the number of times a splitter is met

        Stop when the head goes out of bounds
        """

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
        timelines = 1
        heads = [self.puzzle_input.get_start_position()]

        while heads:
            head = heads[0]

            try:
                below_position = head.below()
                below_symbol = self.puzzle_input.get(below_position)

                if below_symbol == "^":
                    timelines += 1
                    heads.append(below_position.left())
                    heads.append(below_position.right())
                else:
                    heads.append(below_position)
            except IndexError:
                pass

            heads.remove(head)

        return timelines


def main():
    day = Day7()
    day.run()


if __name__ == "__main__":
    main()
