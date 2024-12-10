from utils_aoc import get_filepath_input

HEAD, TAIL = 0, 9
matrix: list[list[int]] = []
heads: list[tuple[int, int]] = []

with open(get_filepath_input(), "r") as file:
    for i, line in enumerate(file.readlines()):
        matrix.append([])
        for j, value in enumerate(map(int, line.strip())):
            matrix[i].append(value)
            if value == HEAD:
                heads.append((i, j))


def get_next_steps(
    matrix: list[list[int]], i_0: int, j_0: int
) -> tuple[tuple[int, int]]:

    return tuple(
        filter(
            lambda pair: matrix[pair[0]][pair[1]] == matrix[i_0][j_0] + 1,
            filter(
                lambda x: 0 <= x[0] < len(matrix)
                and 0 <= x[1] < len(matrix[0]),
                (
                    (i_0 - 1, j_0),
                    (i_0, j_0 + 1),
                    (i_0 + 1, j_0),
                    (i_0, j_0 - 1),
                ),
            ),
        )
    )


def get_paths(
    matrix: list[list[int]],
    head: tuple[int, int],
    found: list[tuple[int, int]],
    unique: bool = True,
    n_paths: int = 0,
):
    i, j = head[0], head[1]
    if matrix[i][j] == TAIL:
        if not unique:
            return 1
        if (i, j) not in found:
            found.append((i, j))
            return 1
    if not (next_steps := get_next_steps(matrix, i, j)):
        return 0
    for next_step in next_steps:
        n_paths += get_paths(matrix, next_step, found, unique)
    return n_paths


print(sum(get_paths(matrix, head, []) for head in heads))  # Part 1
print(
    sum(get_paths(matrix, head, [], unique=False) for head in heads)
)  # Part 2
