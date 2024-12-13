from utils_aoc import get_filepath_input

matrix: list[str] = []

with open(get_filepath_input(), "r") as file:
    matrix = [line.strip() for line in file.readlines()]
    m, n = len(matrix), len(matrix[0])


def get_adjacent_plots(
    plot: tuple[int, int], m: int, n: int
) -> tuple[tuple[int, int]]:
    return tuple(
        filter(
            lambda x: 0 <= x[0] < m and 0 <= x[1] < n,
            (
                (plot[0] - 1, plot[1]),
                (plot[0], plot[1] + 1),
                (plot[0] + 1, plot[1]),
                (plot[0], plot[1] - 1),
            ),
        )
    )


def get_region(
    matrix: list[str],
    i: int,
    j: int,
    region: set[tuple[int, int]] | None = None,
) -> set[tuple[int, int]]:

    if region is None:
        region = {(i, j)}
    for adjacent_plot in filter(
        lambda x: matrix[x[0]][x[1]] == matrix[i][j]
        and (x[0], x[1]) not in region,
        get_adjacent_plots((i, j), len(matrix), len(matrix[0])),
    ):
        region.add((adjacent_plot[0], adjacent_plot[1]))
        region = get_region(matrix, adjacent_plot[0], adjacent_plot[1], region)
    return region


regions: dict[str, dict[int, set[tuple[int, int]]]] = dict()
distinct_regions: dict[str, int] = dict()
for i, line in enumerate(matrix):
    for j, kind in enumerate(matrix[i]):
        found = False
        if kind not in regions:
            regions[kind] = {0: get_region(matrix, i, j)}
            distinct_regions[kind] = 1
            continue
        for region, plots in regions[kind].items():
            if (i, j) in plots:
                break
        else:
            regions[kind][distinct_regions[kind]] = get_region(matrix, i, j)
            distinct_regions[kind] += 1


# The number of sides for Part 2 is equal to the number of edges!
# It took me a while to get it :)
# This can definitely be simplified MUCH further, one check per node
# (intersection of 4 plots) should be enough.
def count_edges(plot: tuple[int, int], matrix: list[str]) -> int:
    edges = 0
    i, j = plot
    m, n = len(matrix), len(matrix[0])
    kind = matrix[i][j]
    if (
        (i == 0 or matrix[i - 1][j] != kind)
        and (j == 0 or matrix[i][j - 1] != kind)
    ) or (
        (i != 0 and matrix[i - 1][j] == kind)
        and (j != 0 and matrix[i][j - 1] == kind)
        and (matrix[i - 1][j - 1] != kind)
    ):
        edges += 1
    if (
        (i == 0 or matrix[i - 1][j] != kind)
        and ((j == n - 1) or matrix[i][j + 1] != kind)
        or (
            (i != 0 and matrix[i - 1][j] == kind)
            and (j != n - 1 and matrix[i][j + 1] == kind)
            and (matrix[i - 1][j + 1] != kind)
        )
    ):
        edges += 1
    if (
        ((i == m - 1) or matrix[i + 1][j] != kind)
        and ((j == n - 1) or matrix[i][j + 1] != kind)
        or (
            (i != m - 1 and matrix[i + 1][j] == kind)
            and (j != n - 1 and matrix[i][j + 1] == kind)
            and (matrix[i + 1][j + 1] != kind)
        )
    ):
        edges += 1
    if (
        ((i == m - 1) or matrix[i + 1][j] != kind)
        and (j == 0 or matrix[i][j - 1] != kind)
        or (
            (i != m - 1 and matrix[i + 1][j] == kind)
            and (j != 0 and matrix[i][j - 1] == kind)
            and (matrix[i + 1][j - 1] != kind)
        )
    ):
        edges += 1
    return edges


perimeters: dict[str, dict[int, int]] = dict()
sides: dict[str, dict[int, int]] = dict()
for kind, region in regions.items():
    if kind not in perimeters:
        perimeters[kind] = dict()
    if kind not in sides:
        sides[kind] = dict()
    for region, plots in region.items():
        if region not in perimeters[kind]:
            perimeters[kind][region] = 0
        if region not in sides[kind]:
            sides[kind][region] = 0
        for plot in plots:
            adjacent_plots = get_adjacent_plots(plot, m, n)
            perimeters[kind][region] += len(
                tuple(
                    filter(
                        lambda x: matrix[x[0]][x[1]] != kind, adjacent_plots
                    )
                )
            ) + (4 - len(adjacent_plots))
            sides[kind][region] += count_edges(plot, matrix)


print(
    sum(
        len(regions[kind][region]) * perimeters[kind][region]
        for kind in regions
        for region in regions[kind]
    )
)  # Part 1

print(
    sum(
        len(regions[kind][region]) * sides[kind][region]
        for kind in regions
        for region in regions[kind]
    )
)  # Part 2
