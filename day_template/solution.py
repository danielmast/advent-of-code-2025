import logging
from pathlib import Path

logger = logging.getLogger(__name__)

INPUT = Path(__file__).parent / "input.txt"

type PuzzleInput = list[str]
type PuzzleOutput = int


def read_input(path: Path = INPUT) -> PuzzleInput:
    with open(path) as file:
        return [line.strip() for line in file]


def solve_part1(puzzle_input: PuzzleInput) -> PuzzleOutput:
    raise NotImplementedError


def solve_part2(puzzle_input: PuzzleInput) -> PuzzleOutput:
    raise NotImplementedError


def main():
    logging.basicConfig(level=logging.INFO)

    puzzle_input = read_input()

    answer_part1 = solve_part1(puzzle_input)
    logger.info(f"Answer part 1: {answer_part1}")

    answer_part2 = solve_part2(puzzle_input)
    logger.info(f"Answer part 2: {answer_part2}")


if __name__ == "__main__":
    main()
