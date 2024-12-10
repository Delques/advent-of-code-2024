from utils_aoc import get_filepath_input

antennas: dict[str, list[tuple[int, int]]] = dict()

with open(get_filepath_input(), "r") as file:
    for i, line in enumerate(file.readlines()):
        for j, char in enumerate(line.strip()):
            if char == ".":
                continue
            if char not in antennas:
                antennas[char] = []
            antennas[char].append((i, j))
    m, n = i, j


def add_antinodes(
    antinodes: set[tuple[int, int]],
    antenna_1: tuple[int, int],
    antenna_2: tuple[int, int],
    m: int,
    n: int,
    in_line: bool = False,
) -> None:

    slope = tuple(antenna_2[index] - antenna_1[index] for index in (0, 1))

    if not in_line:
        for offset in (-1, 2):
            if (
                0 <= (antinode_i := antenna_1[0] + offset * slope[0]) <= m
                and 0 <= (antinode_j := antenna_1[1] + offset * slope[1]) <= n
            ):
                antinodes.add((antinode_i, antinode_j))

    else:
        for direction in (-1, 1):
            c = 0
            while (
                0
                <= (antinode_i := antenna_1[0] + c * direction * slope[0])
                <= m
                and 0
                <= (antinode_j := antenna_1[1] + c * direction * slope[1])
                <= n
            ):
                antinodes.add((antinode_i, antinode_j))
                c += 1


def get_antinodes(
    antennas: dict[str, list[tuple[int, int]]],
    m: int,
    n: int,
    in_line: bool = False,
) -> set[tuple[int, int]]:
    antinodes: set[tuple[int, int]] = set()

    for antenna_coordinates in antennas.values():
        for c, antenna_1 in enumerate(antenna_coordinates):
            for antenna_2 in antenna_coordinates[c + 1 :]:
                add_antinodes(antinodes, antenna_1, antenna_2, m, n, in_line)
    return antinodes


print(len(get_antinodes(antennas, m, n)))  # Part 1
print(len(get_antinodes(antennas, m, n, in_line=True)))  # Part 2
