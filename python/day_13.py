import re
from utils_aoc import get_filepath_input

A_TOKENS = 3

with open(get_filepath_input(), "r") as file:
    content = file.read()

buttons = tuple(
    map(
        lambda x: (int(x[0]), int(x[1])),
        re.findall(r"X\+(\d+), Y\+(\d+)", content),
    )
)
prizes = tuple(
    map(
        lambda x: (int(x[0]), int(x[1])),
        re.findall(r"X=(\d+), Y=(\d+)", content),
    )
)
machines = {
    n: {"A": x[0], "B": x[1], "Prize": x[2]}
    for n, x in enumerate(zip(buttons[::2], buttons[1::2], prizes))
}


def get_coefficients(
    machines: dict[int, dict[str, tuple[int, int]]]
) -> dict[int, tuple[float, float]]:

    coefficients: dict[int, tuple[float, float]] = dict()

    for i, machine in machines.items():
        a_x, a_y = machine["A"][0], machine["A"][1]
        b_x, b_y = machine["B"][0], machine["B"][1]
        p_x, p_y = machine["Prize"][0], machine["Prize"][1]

        # Solve the system of equations by substituting a into b.
        # This assumes they are always linearly independent and that
        # there are no division by zero shenanigans.
        a = (b_x * p_y - b_y * p_x) / (b_x * a_y - b_y * a_x)
        b = (p_x - a * a_x) / b_x
        coefficients[i] = (a, b)

    return coefficients


def fit_restrictions(
    coefficients_pair: tuple[float, float], attempt_limit: int = 0
) -> bool:
    return all(
        all(
            (
                x < (attempt_limit + 1) if attempt_limit else True,
                abs(x - int(x)) < 0.001,
            )
        )
        for x in (coefficients_pair[0], coefficients_pair[1])
    )


def get_sum_tokens(
    coefficients: dict[int, tuple[float, float]], attempt_limit: int = 0
) -> int:
    return int(
        sum(
            A_TOKENS * a + b
            for a, b in filter(
                lambda x: fit_restrictions(x, attempt_limit),
                coefficients.values(),
            )
        )
    )


print(get_sum_tokens(get_coefficients(machines), attempt_limit=100))  # Part 1

machines = {
    n: {
        "A": x["A"],
        "B": x["B"],
        "Prize": tuple(map(lambda x: x + 10000000000000, x["Prize"])),
    }
    for n, x in machines.items()
}

print(get_sum_tokens(get_coefficients(machines)))  # Part 2
