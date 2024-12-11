import dataclasses


@dataclasses.dataclass
class Equation:
    test_result: int
    operands: list[int]


def read_input_file(file_Path: str) -> list[Equation]:
    with open(file_Path) as reader:
        lines: list[str] = reader.readlines()
    equations: list[Equation] = list()
    for line in lines:
        test_result, operands = line.strip().split(":")
        operands = operands.strip().split()
        test_result = int(test_result)
        operands = [int(x) for x in operands]
        equations.append(Equation(test_result, operands))
    return equations


def determine_equation_is_valid(test_result: int, operands: list[int]) -> bool:
    """determines if appying addition and multiplication to opeeands
    evaluating them left to right can obtain test_result"""
    if not operands:
        return False
    if len(operands) == 1:
        return test_result == operands[0]
    first, last = operands[:-1], operands[-1]
    multiplication_result, addition_result = False, False
    if test_result % last == 0:
        # we can possibly apply multiplication as the last operation
        multiplication_result: bool = determine_equation_is_valid(
            test_result // last, first
        )
    if test_result - last >= 0:
        # we can possibly apply addition as the last operation
        addition_result: bool = determine_equation_is_valid(test_result - last, first)
    return addition_result or multiplication_result


def solve_part_a(equations: list[Equation]) -> int:
    return sum(
        equation.test_result
        for equation in equations
        if determine_equation_is_valid(equation.test_result, equation.operands)
    )
