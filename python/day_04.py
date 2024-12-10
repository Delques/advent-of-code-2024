# TODO: Refactor this. Add comments to make decisions and intent
# clearer, or just bite the bullet and solve the puzzle by sweeping
# over the matrix' rows, columns and diagonals.

from utils_aoc import get_filepath_input

with open(get_filepath_input(), "r") as file:
    lines = file.readlines()

WORD = "XMAS"
direction_vectors = [(i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j]

matrix: list[list[str]] = []
m, n, search_order = 0, 0, 0
for i, line in enumerate(lines):
    matrix.append([])
    m += 1
    n_line = 0
    for char in line:
        matrix[i].append(char)
        if char == WORD[0]:
            search_order -= 1
        elif char == WORD[-1]:
            search_order += 1
        n_line += 1
    else:
        n = max(n, n_line)

head, order = (WORD[0], WORD) if search_order >= 0 else (WORD[-1], WORD[::-1])


def get_heads(matrix: list[list[int]], head: str) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i in range(len(matrix))
        for j in range(len(line))
        if matrix[i][j] == head
    ]


heads = get_heads(matrix, head)


def is_match(
    i_0: int,
    j_0: int,
    direction: tuple[int, int],
    order: str,
    offset_max: int,
    offset: int = 0,
) -> bool:
    """
    Recursive function because I decided to be stubborn and not just
    sweep the matrix line by line, column by column, diagonal by
    diagonal.

    TODO: Provide actual info in this docstring.
    """

    i, j = i_0 + direction[0] * offset, j_0 + direction[1] * offset

    if matrix[i][j] != order[offset]:
        return False
    if offset >= offset_max:
        return True
    return is_match(i_0, j_0, direction, order, offset_max, offset + 1)


matches = 0
offset_max = len(WORD) - 1
for i_0, j_0 in heads:
    for direction in direction_vectors:

        if not (0 <= i_0 + direction[0] * offset_max < m) or not (
            0 <= j_0 + direction[1] * offset_max < n
        ):
            continue

        if is_match(i_0, j_0, direction, order, offset_max):
            matches += 1

print(matches)  # Part 1


head = "A"
heads = get_heads(matrix, head)

matches = 0
for i_0, j_0 in heads:
    if (i_0 == 0 or i_0 == m - 1) or (j_0 == 0 or j_0 == n - 1):
        continue

    match (matrix[i_0 - 1][j_0 - 1], matrix[i_0 + 1][j_0 + 1]):
        case x if x not in (("M", "S"), ("S", "M")):
            continue
    match (matrix[i_0 + 1][j_0 - 1], matrix[i_0 - 1][j_0 + 1]):
        case x if x not in (("M", "S"), ("S", "M")):
            continue

    matches += 1


print(matches)  # Part 2
