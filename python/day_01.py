from utils_aoc import get_filepath_input

with open(get_filepath_input(), "r") as file:
    content_num = list(map(int, file.read().split()))

list_1, list_2 = sorted(content_num[::2]), sorted(content_num[1::2])

print(sum(abs(n1 - n2) for n1, n2 in zip(list_1, list_2)))  # Part 1

print(
    sum(n * list_1.count(n) * list_2.count(n) for n in set(list_1))
)  # Part 2
