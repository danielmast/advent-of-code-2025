import inspect
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar


logger = logging.getLogger(__name__)

PuzzleInput = TypeVar("PuzzleInput")
PuzzleOutput1 = TypeVar("PuzzleOutput1")
PuzzleOutput2 = TypeVar("PuzzleOutput2")


class Day(ABC, Generic[PuzzleInput, PuzzleOutput1, PuzzleOutput2]):
    def __init__(self, input_path: Path | None = None):
        if input_path is not None:
            self.input_path = input_path
        else:
            self.input_path = Path(inspect.getfile(type(self))).parent / "input.txt"

        self.puzzle_input: PuzzleInput = self.read_input()

    def read_input(self) -> PuzzleInput:
        with open(self.input_path) as file:
            return [line.strip() for line in file]

    @abstractmethod
    def solve_part1(self) -> PuzzleOutput1: ...

    @abstractmethod
    def solve_part2(self) -> PuzzleOutput2: ...

    def run(self):
        logging.basicConfig(level=logging.INFO)

        answer_part1 = self.solve_part1()
        logger.info(f"Answer part 1: {answer_part1}")

        answer_part2 = self.solve_part2()
        logger.info(f"Answer part 2: {answer_part2}")
