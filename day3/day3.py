from dataclasses import dataclass

from day.day import Day, logger


@dataclass
class Bank:
    digits: int

    def largest_joltage_part1(self) -> int:
        digits_str = str(self.digits)
        first = self._largest_digit(int(digits_str[:-1]))
        first_index = digits_str.index(str(first))
        last = self._largest_digit(int(digits_str[first_index + 1 :]))
        return int(f"{first}{last}")

    def largest_joltage(self, length) -> int:
        digits_str = str(self.digits)
        joltage_digits = []
        start = 0

        logger.debug(f"Joltage digits: {joltage_digits}")

        for i in range(length):
            end = -length + 1 + i
            if end != 0:
                substring = digits_str[start : -length + 1 + i]
            else:
                substring = digits_str[start:]

            joltage_digit = self._largest_digit(int(substring))
            joltage_digits.append(joltage_digit)

            start = substring.index(str(joltage_digit)) + start + 1
            logger.debug(
                f"Substring: {substring}, joltage digits: {joltage_digits}, start: {start}"
            )

        return int("".join(str(joltage_digit) for joltage_digit in joltage_digits))

    @staticmethod
    def _largest_digit(digits: int) -> int:
        return max(int(digit_str) for digit_str in set(str(digits)))


class Day3(Day[list[Bank], int, int]):
    def read_input(self) -> list[Bank]:
        with open(self.input_path) as file:
            return [Bank(int(line.strip())) for line in file]

    def solve_part1(self) -> int:
        return sum(bank.largest_joltage(2) for bank in self.puzzle_input)

    def solve_part2(self) -> int:
        return sum(bank.largest_joltage(12) for bank in self.puzzle_input)


def main():
    day = Day3()
    day.run()


if __name__ == "__main__":
    main()
