from functools import reduce
from copy import deepcopy
from utils_aoc import get_filepath_input

with open(get_filepath_input(), "r") as file:
    content = file.read()

DIRECTIONS: dict[str, tuple[int, int]] = {
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "^": (-1, 0),
}

matrix_0: list[list[str]] = []
matrix: list[list[str]] = []
midway_reached = False
commands: str = ""

with open(get_filepath_input(), "r") as file:
    for i, line in enumerate(file.readlines()):
        if len(line) <= 1:
            midway_reached = True
        if not midway_reached:
            matrix_0.append([])
            for j, char in enumerate(line.strip()):
                matrix_0[i].append(char)
                if char == "@":
                    position = [i, j]
        else:
            commands += line.strip()

matrix = deepcopy(matrix_0)


# This should be broken into a couple different functions so that what
# it does is easier to understand and so that deep copies are no longer
# needed with each step in Part 2, as doing that reduces performance.
# The function should also be able to escape earlier than it currently
# is when the push command is not viable.
def push_objects(
    command: str,
    matrix: list[list[str]],
    position: list[int, int],
    attempted: bool = False,
) -> bool:

    direction = DIRECTIONS[command]
    i_0, j_0 = position[0], position[1]
    i, j = position[0] + direction[0], position[1] + direction[1]

    match matrix[i][j], command:
        case "#", _:
            return False
        case ".", _:
            matrix[i_0][j_0], matrix[i][j] = matrix[i][j], matrix[i_0][j_0]
            position[0], position[1] = i, j
            return True
        case "O", _:
            push_objects(command, matrix, [i, j])
        case "[" | "]", "<" | ">":
            push_objects(command, matrix, [i, j])
        case "[" | "]" as half, "^" | "v":
            if not all(
                (
                    push_objects(command, matrix, [i, j]),
                    push_objects(
                        command,
                        matrix,
                        [i, j + (1 if half == "[" else -1)],
                    ),
                )
            ):
                return False

    if not attempted:
        push_objects(command, matrix, position, attempted=True)

    return True


def get_gps(matrix: list[list[str]], char: str) -> int:
    return reduce(
        lambda a, b: a + b,
        map(
            lambda x: x[0] * 100 + x[1],
            (
                (i, j)
                for i in range(len(matrix))
                for j in range(len(matrix[i]))
                if matrix[i][j] == char
            ),
        ),
    )


for command in commands:
    push_objects(command, matrix, position)

print(get_gps(matrix, char="O"))  # Part 1

matrix = []
for i, line in enumerate(matrix_0):
    matrix.append([])
    for j, char in enumerate(matrix_0[i]):
        match char:
            case "O":
                matrix[i].extend(("[", "]"))
            case "@":
                matrix[i].extend(("@", "."))
                position = [i, j * 2]
            case _:
                matrix[i].extend((char, char))

# Unoptimized, but it's working.
for command in commands:
    matrix_previous = deepcopy(matrix)
    if not push_objects(command, matrix, position):
        matrix = matrix_previous

print(get_gps(matrix, char="["))  # Part 2
