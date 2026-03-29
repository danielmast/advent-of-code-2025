import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

INPUT = Path(__file__).parent / "input.txt"

type PuzzleInput = list[IDRange]
type PuzzleOutput = int


@dataclass
class IDRange:
    start: int
    end: int

    @classmethod
    def parse(cls, s: str) -> IDRange:
        start, end = s.split("-")
        return cls(int(start), int(end))

    def invalid_ids(self, use_divisor_range: bool) -> set[int]:
        return {
            product_id
            for product_id in range(self.start, self.end + 1)
            if not self._is_valid_id(product_id, use_divisor_range)
        }

    @staticmethod
    def _is_valid_id(product_id: int, use_divisor_range: bool) -> bool:
        divisor_range = range(2, len(str(product_id)) + 1) if use_divisor_range else [2]

        for divisor in divisor_range:
            if len(str(product_id)) % divisor != 0:
                continue

            part_len = len(str(product_id)) // divisor
            part = str(product_id)[:part_len]

            if str(product_id).count(part) == divisor:
                return False

        return True


def read_input(path: Path = INPUT) -> PuzzleInput:
    with open(path) as file:
        return [IDRange.parse(range_string) for range_string in file.read().split(",")]


def solve_part1(puzzle_input: PuzzleInput) -> PuzzleOutput:
    return sum(sum(id_range.invalid_ids(False)) for id_range in puzzle_input)


def solve_part2(puzzle_input: PuzzleInput) -> PuzzleOutput:
    return sum(sum(id_range.invalid_ids(True)) for id_range in puzzle_input)


def main():
    logging.basicConfig(level=logging.INFO)

    puzzle_input = read_input()

    answer_part1 = solve_part1(puzzle_input)
    logger.info(f"Answer part 1: {answer_part1}")

    answer_part2 = solve_part2(puzzle_input)
    logger.info(f"Answer part 2: {answer_part2}")


if __name__ == "__main__":
    main()
