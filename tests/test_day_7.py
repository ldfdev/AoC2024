from aoc import day7
from pathlib import Path

day_5_file: Path = Path(__file__).parent / "day7.input"
input_data: list[day7.Equation] = day7.read_input_file(day_5_file.as_posix())


def test_determine_equation_is_valid():
    allowed_operations: list[day7.Operation] = [
        day7.Operation.ADDITION,
        day7.Operation.MULTIPLICATION,
    ]
    assert day7.determine_equation_is_valid(100, [10, 10], allowed_operations) is True
    assert (
        day7.determine_equation_is_valid(110, [10, 10, 10], allowed_operations) is True
    )
    assert day7.determine_equation_is_valid(10, [10], allowed_operations) is True

    assert day7.determine_equation_is_valid(100, [1, 10], allowed_operations) is False
    assert day7.determine_equation_is_valid(54, [10], allowed_operations) is False

    assert day7.determine_equation_is_valid(1212, [12, 12], allowed_operations) is False
    assert day7.determine_equation_is_valid(1212, [12, 12], [op for op in day7.Operation]) is True

def test_solve_part_a():
    assert day7.solve_part_a(input_data) == 3749

def test_solve_part_b():
    assert day7.solve_part_b(input_data) == 11387
