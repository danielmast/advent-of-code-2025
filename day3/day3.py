from dataclasses import dataclass

from day.day import Day, logger


@dataclass
class Bank:
    digits: str

    def largest_joltage(self, length) -> int:
        joltage_digits = []
        start = 0

        for i in range(length):
            remaining = length - 1 - i
            end = len(self.digits) - remaining if remaining > 0 else None
            substring = self.digits[start:end]

            joltage_digit = max(substring)
            joltage_digits.append(joltage_digit)

            start = substring.index(joltage_digit) + start + 1

            logger.debug(
                f"Substring: {substring}, joltage digits: {joltage_digits}, start: {start}"
            )

        return int("".join(joltage_digits))


class Day3(Day[list[Bank], int, int]):
    def read_input(self) -> list[Bank]:
        with open(self.input_path) as file:
            return [Bank(line.strip()) for line in file]

    def sum_of_largest_joltages(self, length: int) -> int:
        return sum(bank.largest_joltage(length) for bank in self.puzzle_input)

    def solve_part1(self) -> int:
        return self.sum_of_largest_joltages(2)

    def solve_part2(self) -> int:
        return self.sum_of_largest_joltages(12)


def main():
    day = Day3()
    day.run()


if __name__ == "__main__":
    main()
