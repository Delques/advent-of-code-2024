from utils.get_filepath_input import get_filepath_input

DAY_NUMBER = 9

files: dict[int, int] = dict()
files_positions: dict[int, int] = dict()
free_spaces: dict[int, int] = dict()
compacted: list[int | str] = []
c = 0
files_positions_count = 0
with open(get_filepath_input(DAY_NUMBER)) as file:
    for i, value in enumerate(map(int, file.read().strip())):
        if i % 2 == 0:
            files_positions[c] = len(compacted)
            compacted.extend(c for _ in range(value))
            files[c] = value
            c += 1
            files_positions_count += value
        else:
            if value:
                free_spaces[len(compacted)] = value
            compacted.extend("." for _ in range(value))

compacted_1 = compacted[:]
compacted_2 = compacted[:]

n = len(compacted)
first_free_space = 0
for k, file_index in enumerate(reversed(compacted)):
    if file_index == ".":
        continue
    if k >= files_positions_count:
        break
    for i in range(first_free_space, n):
        if compacted_1[i] != ".":
            continue
        compacted_1[i] = file_index
        first_free_space = i
        break


def get_checksum(compacted: list[int | str]) -> int:
    return sum(
        i * value
        for i, value in enumerate(compacted)
        if isinstance(value, int)
    )


print(get_checksum(compacted_1[:files_positions_count]))  # Part 1

ordered_free_spaces = sorted(free_spaces)

for f in reversed(range(len(files))):

    for possible_space in ordered_free_spaces:
        if (
            files[f] <= free_spaces[possible_space]
            and files_positions[f] > possible_space
        ):
            index = possible_space
            for i in range(files[f]):
                compacted_2[index + i] = f
                compacted_2[files_positions[f] + i] = "."
            if new_space := free_spaces[possible_space] - files[f]:
                free_spaces[index + i + 1] = new_space
                ordered_free_spaces.insert(
                    ordered_free_spaces.index(index), index + i + 1
                )
            del free_spaces[index]
            ordered_free_spaces.remove(index)
            break

print(get_checksum(compacted_2))  # Part 2
