import dataclasses
import typing
import enum


@dataclasses.dataclass
class Equation:
    test_result: int
    operands: list[int]


class Operation(enum.Enum):
    ADDITION = enum.auto()
    MULTIPLICATION = enum.auto()
    CONCATENATION = enum.auto()


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


def apply_addition(term_1: int, term_2: int) -> typing.Optional[int]:
    """Checks if ot is possible to apply addition between the 2 terms
    If so, return the modified term_1 as the result
    Otehrwise return None"""
    if term_1 - term_2 >= 0:
        return term_1 - term_2


def apply_multiplication(term_1: int, term_2: int) -> typing.Optional[int]:
    """Checks if ot is possible to apply multiplication between the 2 terms
    If so, return the modified term_1 as the result
    Otehrwise return None"""
    if term_1 % term_2 == 0:
        return term_1 // term_2


def apply_concatenation(term_1: int, term_2: int) -> typing.Optional[int]:
    """Checks if ot is possible to apply concatenation between the 2 terms
    If so, return the modified term_1 as the result
    Otehrwise return None"""
    str_term_1, str_term_2 = str(term_1), str(term_2)
    if str_term_1.endswith(str_term_2):
         pref: str = str_term_1.removesuffix(str_term_2)
         if pref:
             return int(pref)


def determine_equation_is_valid(
    test_result: int, operands: list[int], allowed_operations: list[Operation]
) -> bool:
    """determines if appying addition and multiplication to opeeands
    evaluating them left to right can obtain test_result"""
    if not operands:
        return False
    if len(operands) == 1:
        return test_result == operands[0]
    first, last = operands[:-1], operands[-1]

    operation_results: list[bool] = list()

    if Operation.MULTIPLICATION in allowed_operations:
        multiplication_result = apply_multiplication(test_result, last)
        if multiplication_result is not None:
            multiplication_solution: bool = determine_equation_is_valid(
                multiplication_result, first, allowed_operations
            )
            operation_results.append(multiplication_solution)

    if Operation.ADDITION in allowed_operations:
        addition_result = apply_addition(test_result, last)
        if addition_result is not None:
            addition_solution: bool = determine_equation_is_valid(
                addition_result, first, allowed_operations
            )
            operation_results.append(addition_solution)

    if Operation.CONCATENATION in allowed_operations:
        concatenation_result = apply_concatenation(test_result, last)
        if concatenation_result is not None:
            concatenationsolution: bool = determine_equation_is_valid(
                concatenation_result, first, allowed_operations
            )
            operation_results.append(concatenationsolution)

    return any(operation_results)


def solve_part_a(equations: list[Equation]) -> int:
    return sum(
        equation.test_result
        for equation in equations
        if determine_equation_is_valid(
            equation.test_result,
            equation.operands,
            [Operation.ADDITION, Operation.MULTIPLICATION],
        )
    )

def solve_part_b(equations: list[Equation]) -> int:
    return sum(
        equation.test_result
        for equation in equations
        if determine_equation_is_valid(
            equation.test_result,
            equation.operands,
            [Operation.ADDITION, Operation.MULTIPLICATION, Operation.CONCATENATION],
        )
    )