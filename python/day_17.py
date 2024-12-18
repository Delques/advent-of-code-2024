from collections.abc import Callable
from utils_aoc import get_filepath_input

global registers
global position
global jumped
global output

registers: dict[str, int] = {"A": 0, "B": 0, "C": 0}
program: list[int] = []
with open(get_filepath_input(), "r") as file:
    for line in file.readlines():
        for k in registers:
            if line.startswith(f"Register {k}:"):
                registers[k] = int(line.strip().split(":")[1])
                break
        else:
            if line.startswith("Program:"):
                program: tuple[int] = tuple(
                    map(int, line.strip().split(":")[1].split(","))
                )


operands: dict[str, dict[int, int | Callable[[], int]]] = dict()
OPERANDS_REGISTERS: dict[int, str] = {4: "A", 5: "B", 6: "C"}

for operand_type in ("literal", "combo"):
    operands[operand_type] = dict()
    for i in range(8):
        if operand_type == "literal":
            operands[operand_type][i] = i
            continue
        if i in OPERANDS_REGISTERS:
            operands[operand_type][i] = lambda i: registers.get(
                OPERANDS_REGISTERS[i]
            )
            continue
        operands[operand_type][i] = lambda i: operands["literal"].get(i)


instructions: dict[int, Callable] = dict()
pointer: list[int] = [0]
output: list[str] = [""]
jumped: list[bool] = [False]


def adv(operand: int) -> None:
    registers["A"] //= 2 ** operands["combo"][operand](operand)


def bxl(operand: int) -> None:
    registers["B"] ^= operands["literal"][operand]


def bst(operand: int) -> None:
    registers["B"] = operands["combo"][operand](operand) % 8


def jnz(operand: int) -> None:
    if not registers["A"]:
        return
    pointer[0] = operands["literal"][operand]
    jumped[0] = True


def bxc(operand: int) -> None:
    registers["B"] ^= registers["C"]


def out(operand: int) -> None:
    output[
        0
    ] += f"{"," if output[0] else ""}{operands["combo"][operand](operand) % 8}"


def bdv(operand: int) -> None:
    registers["B"] = registers["A"] // (
        2 ** operands["combo"][operand](operand)
    )


def cdv(operand: int) -> None:
    registers["C"] = registers["A"] // (
        2 ** operands["combo"][operand](operand)
    )


opcodes: dict[int, Callable[[int], None]] = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def execute_program(program: tuple[int], equals_program: bool = False) -> None:
    out_calls = 0
    out_called = False
    keep_running = True
    while keep_running:

        if pointer[0] + 1 >= len(program):
            break
        if equals_program and out_calls > len(program):
            break
        if equals_program and program[pointer[0]] == 5:
            out_calls += 1
            out_called = True

        opcodes[program[pointer[0]]](program[pointer[0] + 1])

        if out_called:
            for i in range(out_calls):
                if int(output[0][i * 2]) != program[i]:
                    keep_running = False
                    break
            out_called = False

        if jumped[0]:
            jumped[0] = False
            continue
        else:
            pointer[0] += 2


execute_program(program)

print(output[0])  # Part 1
