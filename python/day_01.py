from utils.get_filepath_input import get_filepath_input

DAY_NUMBER = 1

filepath_input = get_filepath_input(DAY_NUMBER)

with open(filepath_input, "r") as file:
    content_num = list(map(int, file.read().split()))

list_1, list_2 = sorted(content_num[::2]), sorted(content_num[1::2])

score_difference = sum(abs(n1 - n2) for n1, n2 in zip(list_1, list_2))

print(score_difference)  # Part 1

score_similarity = sum(
    n * list_1.count(n) * list_2.count(n) for n in set(list_1)
)

print(score_similarity)  # Part 2
