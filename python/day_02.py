from typing import Generator
from utils_aoc import get_filepath_input

with open(get_filepath_input(), "r") as file:
    matrix = [[int(x) for x in line.split()] for line in file.readlines()]


def is_safe_report(
    report: list[int], min_dif: int = 1, max_dif: int = 3
) -> bool:
    """
    Given a report, determine whether it is safe. The report (a list
    of integers) is safe it its values are always increasing/decreasing
    and if the differences between adjacent elements in the list are
    always between 'min' and 'max'.

    Args:
        report (list[int]):
            List of levels in the report.
        min_dif (int = 1):
            Minimum difference between adjacent levels in a safe
            report.
        max_dif (int = 3):
            Maximum difference between adjacent levels in a safe
            report.

    Returns:
        True if the report is safe, False otherwise.
    """

    ascending = None
    for i in range(1, len(report)):
        dif = report[i] - report[i - 1]
        if min_dif <= dif <= max_dif and (ascending or ascending is None):
            ascending = True
        elif -max_dif <= dif <= -min_dif and (
            not ascending or ascending is None
        ):
            ascending = False
        else:
            return False
    return True


safe_reports = sum(is_safe_report(report) for report in matrix)

print(safe_reports)  # Part 1


def generate_subsets(report: list[int]) -> Generator[list[int], None, None]:
    """
    Given a report, generate a list of that report's subsets which do
    not contain exactly one of its elements.

    Args:
        report (list[int]): List of levels in a report.

    Yields:
        A list of subsets of the report, each lacking one of its
        elements in comparison.
    """

    yield from (report[:n] + report[n + 1 :] for n in range(len(report)))


safe_reports = sum(
    any(is_safe_report(subset) for subset in generate_subsets(report))
    for report in matrix
)

print(safe_reports)  # Part 2
