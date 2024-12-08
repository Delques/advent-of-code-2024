from typing import Callable
from operator import add, mul
from utils.get_filepath_input import get_filepath_input

DAY_NUMBER = 7

filepath_input = get_filepath_input(DAY_NUMBER)

results: list[int] = []
terms: list[list[int]] = []
with open(filepath_input, "r") as file:
    for line in file.readlines():
        results.append(int(line.split(":")[0]))
        terms.append(list(map(int, line.split(":")[1].split())))


# There are probably much better ways to do combinatorics and this is
# probably not even the way to go for solving this, but I am using base
# conversion as a proxy for mapping all the possibilities of operator
# sequences.
def convert_base(i: int, b: int, chars: int) -> str:
    n = 0
    while i > b**n:
        n += 1
    r = i
    converted = ""
    while n >= 0:
        q = r // (b**n)
        r = r % (b**n)
        converted += f"{q}"
        n -= 1
    return f"{converted:0>{chars}}"[-chars:]


def get_calibration_result(
    results: list[int],
    terms: list[list[int]],
    operators: dict[str, Callable[[int, int], int]],
) -> int:

    calibration_result = 0

    for result, terms in zip(results, terms):
        sequences = (
            (operators[k] for k in convert_base(i, len(operators), len(terms)))
            for i in range(len(operators) ** len(terms))
        )
        for sequence in sequences:
            result_int = terms[0]
            for operator, term in zip(sequence, terms[1:]):
                result_int = operator(result_int, term)
                if result_int > result:
                    break
            if result_int == result:
                calibration_result += result
                break

    return calibration_result


operators = {"0": add, "1": mul}

print(get_calibration_result(results, terms, operators))  # Part 1


def concatenate(a: int, b: int) -> int:
    return int(f"{a}{b}")


operators.update({"2": concatenate})

# Very unoptimized, but it's working
print(get_calibration_result(results, terms, operators))  # Part 2
