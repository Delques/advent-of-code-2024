from utils.get_filepath_input import get_filepath_input

DAY_NUMBER = 1

filepath_input = get_filepath_input(DAY_NUMBER)

with open(filepath_input, "r") as file:
    content = file.readlines()

list_1 = []
list_2 = []
for line in content:
    line_numbers = list(map(int, line.split()))
    list_1.append(line_numbers[0])
    list_2.append(line_numbers[1])

list_1.sort()
list_2.sort()

sum_differences = 0
for n1, n2 in zip(list_1, list_2):
    sum_differences += abs(n1 - n2)

print(sum_differences)  # Part 1

number_similarity_score = dict()
for n in list_1:
    if n in number_similarity_score:
        continue
    number_similarity_score[n] = n * list_1.count(n) * list_2.count(n)
total_similarity_score = sum(list(number_similarity_score.values()))

print(total_similarity_score)  # Part 2
