import re
from typing import cast
from utils.get_filepath_input import get_filepath_input

DAY_NUMBER = 5

filepath_input = get_filepath_input(DAY_NUMBER)

with open(filepath_input, "r") as file:
    content = file.read()


order: dict[str, list[str]] = dict()
for pair in cast(list[tuple[str, str]], re.findall(r"(.+)\|(.+)", content)):
    if pair[0] not in order:
        order[pair[0]] = []
    order[pair[0]].append(pair[1])


updates = map(
    lambda x: list(x.strip().split(",")),
    cast(list[str], re.findall(r"\d+,.*(?:\s+|\Z)", content)),
)


def is_ordered(update: list[str], order: dict[str, list[str]]) -> bool:
    for i, last in zip(range(1, len(update)), update[1:]):
        for first in update[:i]:
            if first in order.get(last, ""):
                return False
    return True


def get_sum_middle(updates: list[list[str]]) -> int:
    return sum(int(update[len(update) // 2]) for update in updates)


updates_ordered: list[list[str]] = []
updates_unordered: list[list[str]] = []
for update in updates:
    if is_ordered(update, order):
        updates_ordered.append(update)
    else:
        updates_unordered.append(update)

print(get_sum_middle(updates_ordered))  # Part 1


# TODO: Refactor this and is_ordered, maybe abstract a third function
# for the loop.
def reorder_update(
    update: list[str], order: dict[str, list[str]]
) -> list[str]:
    for i_l, last in zip(range(1, len(update)), update[1:]):
        for i_f, first in enumerate(update[:i_l]):
            if first in order.get(last, ""):
                update.insert(i_f, update.pop(i_l))
                break
    return update


updates_unordered = [
    reorder_update(update, order) for update in updates_unordered
]

print(get_sum_middle(updates_unordered))  # Part 2
