from itertools import cycle
from typing import Iterator, Literal
from utils_aoc import get_filepath_input

obstructions: set[tuple[int, int]] = set()
matrix: list[str] = []

with open(get_filepath_input(), "r") as file:
    for i, line in enumerate(file.readlines()):
        matrix.append(line.strip())
        for j, char in enumerate(matrix[i]):
            match char:
                case ".":
                    continue
                case "#":
                    obstructions.add((i, j))
                case "^":
                    i_0, j_0 = i, j
    m, n = i, j


def traverse(
    i: int,
    j: int,
    m: int,
    n: int,
    directions: Iterator[tuple[int, int]],
    obstructions: set[tuple[int, int]],
    check_loops: bool = False,
) -> set[tuple[int, int]] | Literal[-1]:

    direction = next(directions)
    traversed: set[tuple[int, int]] = set()

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

# A bit unoptimized, but it's working
possible_obstructions = 0
for k, position in enumerate(traversed):

    obstructions_new = obstructions | {tuple((position[0], position[1]))}
    directions = cycle(((-1, 0), (0, 1), (1, 0), (0, -1)))

    if traverse(i_0, j_0, m, n, directions, obstructions_new, True) == -1:
        possible_obstructions += 1

print(possible_obstructions)  # Part 2
