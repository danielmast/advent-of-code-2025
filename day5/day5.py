from dataclasses import dataclass
from pathlib import Path

from day.day import Day


@dataclass(frozen=True, order=True)
class IDRange:
    start: int
    end: int

    def __contains__(self, id: int) -> bool:
        return self.start <= id <= self.end

    def __len__(self):
        return self.end - self.start + 1

    def mergeable_with(self, other: IDRange) -> bool:
        return self.start <= other.end and other.start <= self.end + 1

    def merge_with(self, other: IDRange) -> IDRange:
        return IDRange(min(self.start, other.start), max(self.end, other.end))


@dataclass
class IngredientInfo:
    fresh_id_ranges: list[IDRange]
    available_ids: list[int]

    @classmethod
    def parse_file(cls, path: Path) -> IngredientInfo:
        fresh_id_ranges = []
        available_ids = []
        with open(path) as file:
            for line in file:
                line = line.strip()
                if "-" in line:
                    start, end = map(int, line.split("-"))
                    fresh_id_ranges.append(IDRange(start, end))
                elif not line:
                    continue
                else:
                    available_ids.append(int(line))

        return cls(fresh_id_ranges, available_ids)

    def is_fresh_id(self, id: int) -> bool:
        return any(id in r for r in self.fresh_id_ranges)

    def num_fresh_and_available_ids(self) -> int:
        return sum(1 for id in self.available_ids if self.is_fresh_id(id))

    def fresh_id_ranges_without_overlap(self) -> list[IDRange]:
        new_ranges = []
        for r in sorted(self.fresh_id_ranges):
            if new_ranges and new_ranges[-1].mergeable_with(r):
                new_ranges[-1] = new_ranges[-1].merge_with(r)
            else:
                new_ranges.append(r)
        return new_ranges

    def num_fresh_ids(self) -> int:
        return sum(len(id_range) for id_range in self.fresh_id_ranges_without_overlap())


class Day5(Day):
    def read_input(self) -> IngredientInfo:
        return IngredientInfo.parse_file(self.input_path)

    def solve_part1(self) -> int:
        return self.puzzle_input.num_fresh_and_available_ids()

    def solve_part2(self) -> int:
        return self.puzzle_input.num_fresh_ids()


def main():
    day = Day5()
    day.run()


if __name__ == "__main__":
    main()
