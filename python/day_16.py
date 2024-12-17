# Not my best solution, but it's past midnight already.
# It takes a couple of minutes to run in my PC.
from utils_aoc import get_filepath_input
import sys

sys.setrecursionlimit(10000)  # Yeah... it's not very performant.

matrix: list[list[str]] = []

with open(get_filepath_input(), "r") as file:
    for i, line in enumerate(file.readlines()):
        matrix.append([])
        for j, char in enumerate(line.strip()):
            matrix[i].append(char)
            if char == "S":
                start = (i, j)
            elif char == "E":
                end = (i, j)
    N = j

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


found_paths: list[set[tuple[int, tuple[int, int]]]] = []
minimums: dict[int, int] = dict()
k = 0
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        minimums[k] = 999999999
        k += 1


def get_key(position: tuple[int, int]):
    return position[0] * (N - 1) + position[1] - 1


def move_reindeer(
    position: tuple[int, int],
    direction: tuple[int, int],
    matrix: list[list[str]],
    found_paths: list[set[tuple[int, tuple[int, int]]]] = None,
    current_sum: int = 0,
    path: set[tuple[int, int]] = None,
    use_paths: list[set[tuple[int, int]]] = None,
    off_path: int = 0,
) -> None:

    if use_paths:
        if position not in use_paths:
            off_path += 1
        if off_path > 15:  # Weigh against going off the beaten path.
            off_path = 0
            return

    if matrix[position[0]][position[1]] == "E":
        found_paths.append((current_sum, path))

    next_position = (position[0] + direction[0], position[1] + direction[1])

    if not use_paths:
        if current_sum > minimums[get_key(position)]:
            path.add(position)
            return
        else:
            minimums[get_key(position)] = current_sum
    else:
        if current_sum <= minimums[get_key(position)]:
            minimums[get_key(position)] = current_sum

    path.add(position)

    for next_direction in DIRECTIONS:
        next_position = (
            position[0] + next_direction[0],
            position[1] + next_direction[1],
        )

        if next_position in path:
            continue

        match matrix[next_position[0]][next_position[1]]:
            case "#":
                continue

        move_reindeer(
            next_position,
            next_direction,
            matrix,
            found_paths,
            current_sum + (1 if next_direction == direction else 1001),
            path.copy(),
            use_paths,
            off_path,
        )


move_reindeer(start, DIRECTIONS[0], matrix, found_paths, 0, set())
print(minimums[get_key(end)])  # Part 1

path_tiles: set[tuple[int, int]] = set()
for path in found_paths:
    if path[0] == minimums[get_key(end)]:
        for tile in path[1]:
            path_tiles.add(tile)
path_tiles.add(start)
path_tiles.add(end)


move_reindeer(start, DIRECTIONS[0], matrix, found_paths, 0, set(), path_tiles)

path_tiles: set[tuple[int, int]] = set()
for path in found_paths:
    if path[0] == minimums[get_key(end)]:
        for tile in path[1]:
            path_tiles.add(tile)
path_tiles.add(start)
path_tiles.add(end)

print(len(path_tiles))  # Part 2
