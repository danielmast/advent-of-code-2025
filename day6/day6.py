import math
from dataclasses import dataclass
from enum import Enum

from day.day import Day


class Operator(Enum):
    MULTIPLY = "*"
    ADD = "+"


@dataclass
class Problem:
    numbers: list[int]
    operator: Operator | None

    def add_number(self, number: int) -> None:
        self.numbers.append(number)

    def solve(self) -> int:
        if self.operator == Operator.MULTIPLY:
            return math.prod(self.numbers)
        else:
            return sum(self.numbers)


@dataclass
class PuzzleInputs:
    part1: list[Problem]
    part2: list[Problem]


class Day6(Day):
    def read_input(self) -> PuzzleInputs:
        return PuzzleInputs(self.read_input_part1(), self.read_input_part2())

    def read_input_part1(self) -> list[Problem]:
        problems = []
        with open(self.input_path) as file:
            for line in file:
                if "+" not in line:
                    numbers = [int(n) for n in line.split()]

                    if not problems:
                        problems = [Problem([number], None) for number in numbers]
                    else:
                        for i, number in enumerate(numbers):
                            problems[i].add_number(number)
                else:
                    operators = [Operator(o) for o in line.split()]
                    for i, operator in enumerate(operators):
                        problems[i].operator = operator

        return problems

    def read_input_part2(self) -> list[Problem]:
        with open(self.input_path) as file:
            lines = [line.rstrip("\n") for line in file]

        transposed = ["".join(row) for row in zip(*lines)]

        problems = []
        problem = Problem([], None)
        for line in transposed:
            if line.isspace():
                problems.append(problem)
                problem = Problem([], None)
                continue
            elif "+" in line:
                problem.operator = Operator.ADD
                line = line.replace("+", "")
            elif "*" in line:
                problem.operator = Operator.MULTIPLY
                line = line.replace("*", "")

            number = int(line.strip())

            problem.add_number(number)

        problems.append(problem)

        return problems

    def solve_part1(self) -> int:
        return sum(problem.solve() for problem in self.puzzle_input.part1)

    def solve_part2(self) -> int:
        return sum(problem.solve() for problem in self.puzzle_input.part2)


def main():
    day = Day6()
    day.run()


if __name__ == "__main__":
    main()
