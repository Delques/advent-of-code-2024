from itertools import cycle
from typing import Iterator, Literal, cast
from utils.get_filepath_input import get_filepath_input

DAY_NUMBER = 6

filepath_input = get_filepath_input(DAY_NUMBER)

obstructions: list[tuple[int, int]] = []

matrix: list[str] = []
with open(filepath_input, "r") as file:
    for i, line in enumerate(file.readlines()):
        matrix.append(line.strip())
        for j, char in enumerate(matrix[i]):
            match char:
                case ".":
                    continue
                case "#":
                    obstructions.append((i, j))
                case "^":
                    i_0, j_0 = i, j
        else:
            n = j
    else:
        m = i


def traverse(
    i: int,
    j: int,
    m: int,
    n: int,
    directions: Iterator[tuple[tuple[int, int]]],
    obstructions: list[tuple[int, int]],
    check_loops: bool = False,
) -> set[tuple[int, int]] | Literal[-1]:

    direction = next(directions)
    traversed = set()
    if not check_loops:
        traversed = cast(set[tuple[int, int]], traversed)
    else:
        traversed = cast(
            set[tuple[int, int, tuple[tuple[int, int]]]], traversed
        )

    while True:

        if not (0 <= i <= m) or not (0 <= j <= n):
            break

        if not check_loops:
            if (i, j) not in traversed:
                traversed.add((i, j))
        else:
            if (i, j, direction) not in (traversed):
                traversed.add((i, j, direction))
            else:
                return -1

        i_next, j_next = i + direction[0], j + direction[1]
        if (i_next, j_next) in obstructions:
            direction = next(directions)
            continue
        i, j = i_next, j_next

    return traversed


directions = cycle(((-1, 0), (0, 1), (1, 0), (0, -1)))
traversed = traverse(i_0, j_0, m, n, directions, obstructions)

print(len(traversed))  # Part 1

# Really unoptimized, but it works
possible_obstructions = 0
for position in traversed:

    obstructions_new = obstructions[:] + [(position[0], position[1])]
    directions = cycle(((-1, 0), (0, 1), (1, 0), (0, -1)))

    if traverse(i_0, j_0, m, n, directions, obstructions_new, True) == -1:
        possible_obstructions += 1

print(possible_obstructions)  # Part 2
