import inspect
from pathlib import Path
from typing import Generic, TypeVar


from day.day import Day, PuzzleInput, PuzzleOutput1, PuzzleOutput2

INPUT = "input.txt"
EXAMPLE_INPUT = "example_input.txt"


class DayTest(Generic[PuzzleInput, PuzzleOutput1, PuzzleOutput2]):
    day_class: type[Day]
    example_answer_part1: PuzzleOutput1
    example_answer_part2: PuzzleOutput2
    answer_part1: PuzzleOutput1
    answer_part2: PuzzleOutput2

    def make_day(self, filename: str) -> Day:
        path = Path(inspect.getfile(self.day_class)).parent / filename
        return self.day_class(input_path=path)

    def test_solve_part1_example(self):
        day = self.make_day(EXAMPLE_INPUT)
        assert day.solve_part1() == self.example_answer_part1

    def test_solve_part2_example(self):
        day = self.make_day(EXAMPLE_INPUT)
        assert day.solve_part2() == self.example_answer_part2

    def test_solve_part1(self):
        day = self.make_day(INPUT)
        assert day.solve_part1() == self.answer_part1

    def test_solve_part2(self):
        day = self.make_day(INPUT)
        assert day.solve_part2() == self.answer_part2
