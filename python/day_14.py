import re
from typing import cast
from functools import reduce
from utils_aoc import get_filepath_input

M, N = 103, 101
SECONDS = 100
positions: list[tuple[int, int]] = []
velocities: list[tuple[int, int]] = []

with open(get_filepath_input(), "r") as file:
    for position, velocity in cast(
        list[tuple[str, str]],
        re.findall(r"p=([\d,]+) v=([\d,-]+)", file.read()),
    ):
        positions.append(tuple(map(int, position.split(",")[::-1])))
        velocities.append(tuple(map(int, velocity.split(",")[::-1])))


def get_final_position(
    p_0: tuple[int, int], v: tuple[int, int], t: int, m: int, n: int
) -> tuple[int, int]:

    return (p_0[0] + v[0] * t) % m, (p_0[1] + v[1] * t) % n


final_positions = (
    get_final_position(p, v, SECONDS, M, N)
    for p, v in zip(positions, velocities)
)

quadrants = [0, 0, 0, 0]
for p in tuple(
    filter(lambda p: p[0] != M // 2 and p[1] != N // 2, final_positions)
):
    match p[0] < M // 2, p[1] < N // 2:
        case True, True:
            quadrants[0] += 1
        case True, False:
            quadrants[1] += 1
        case False, True:
            quadrants[2] += 1
        case False, False:
            quadrants[3] += 1

print(reduce(lambda x, y: x * y, quadrants))  # Part 1


def print_positions(positions: list[tuple[int, int]], m: int, n: int) -> None:
    matrix = ""
    for i in range(m):
        for j in range(n):
            if (i, j) in positions:
                matrix += "*"
            else:
                matrix += " "
        else:
            matrix += "\n"
    print(matrix)


from time import sleep

t = 0
while True:  # Ctrl + C to break
    user_input = input("Begin printing charts (y/n)? ")
    if user_input.lower() == "n":
        break
    positions_t = list(
        get_final_position(p, v, t, M, N)
        for p, v in zip(positions, velocities)
    )
    print_positions(positions_t, M, N)
    print(f"Above is a depiction of the chart after {t} seconds.\n")
    t += 1
    sleep(0.10)

# Part 2? I have no idea if it was meant to be subjective like this.
# My input generated the following Christmas tree after 7916 iterations
# and a bunch of attempted false positives/going for different regions
# and speeds:

#                                                                                     *

#                                         *
#                                                                                 *

#    *                                       *                                     *    *
#                                                                            *
#    * *                                                             *
#                                                                               *
#                                                                                               *


#                                                  *


#     *                                                          *
#                                                                              *
#                    *******************************                                           *
#                    *                             *           *           *   *
#          *         *                             *        *                 *
#                    *                             *
#                    *                             *                    *
#                    *              *              *   *    *
#           *        *             ***             *
#              *     *            *****            *
#                    *           *******           *                        *
#                    *          *********          *  *
#                    *            *****            *
#                    *           *******           *
#                    *          *********          *                        *
#                    *         ***********         *                                         *     *
#                    *        *************        *
#                    *          *********          *
#                    *         ***********         *              *
#                    *        *************        *                   *
#                    *       ***************       *                                               *
#                    *      *****************      *             *
#                    *        *************        *
#      *             *       ***************       *                     *
#          *         *      *****************      *
#                    *     *******************     *
#                    *    *********************    *                                               *
#                    *             ***             *                                            *
#                    *             ***             *
#                    *             ***             *               *             *                   *
#                    *                             *                                   *
#                    *                             *        *
#                    *                             *
#                    *                             *                                       *
#                    *******************************                             *
#                                                            *
#                                                          *                      *
#                     *   *


#                     *     *                                      *                              *
#                                *
#                                                         *    *                                *
#                                   *                                      *                *
#             *                                                    *
#             *                                                                                    *
#               *                 *                             *


#                                        *                   *              *
#                               *
#                                            *                         *                  *          *
#                                   * *                    *               *
#                                                                *
#                      *
#                                                         *                                        *

#                             *                                                                 *
#                                               *                *

#   *                               *     *                      *

#                *                                                                           *
#                                   *
#                                                                           *        *
#                                        *
#                                                *
#             **
#            *                   *    *                                                  *          *
#                  *                                                                         *

#          *                       *                                    *                     *
#                                                                                 *    *

#            *                                                *                                    *
#                                                                                *  **        *
#                    *
#                                                  *
#                                                                          *    *
#                                                                                      *

#                       *                     *              *                                      *
#                                                                                            **       *

#                                            *
#                                 *        *                                                      *
#   *                                                                                            *
#       *                                                                                       *    *
