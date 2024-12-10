import re
from utils_aoc import get_filepath_input

with open(get_filepath_input(), "r") as file:
    content = file.read()


def get_sum_of_products(
    memory_code: str, use_conditionals: bool = False
) -> int:
    """
    Given a piece of memory code, get the sum of the results of each
    'mul(a, b)' operation. If using conditionals, ignore code set after
    'don't()' commands.

    Args:
        memory_code (str):
            Piece of scanned memory.
        use_conditionals (bool = False):
            Flag on whether to consider 'do()' and 'don't()' commands.

    Returns:
        The sum of multiplications in the memory code.
    """

    if use_conditionals:
        memory_code = re.sub(
            r"don't().*?(?=do()|\Z)", "", memory_code, flags=re.S
        )

    return sum(
        map(
            lambda pair: int(pair[0]) * int(pair[1]),
            re.findall(r"mul\((\d+),(\d+)\)", memory_code),
        )
    )


print(get_sum_of_products(content))  # Part 1
print(get_sum_of_products(content, use_conditionals=True))  # Part 2
