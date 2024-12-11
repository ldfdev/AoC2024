from aoc import day7
from pathlib import Path

day_5_file: Path = Path(__file__).parent / "day7.input"
input_data: list[day7.Equation] = day7.read_input_file(day_5_file.as_posix())


def test_determine_equation_is_valid():
    assert day7.determine_equation_is_valid(100, [10, 10]) is True
    assert day7.determine_equation_is_valid(110, [10, 10, 10]) is True
    assert day7.determine_equation_is_valid(10, [10]) is True

    assert day7.determine_equation_is_valid(100, [1, 10]) is False
    assert day7.determine_equation_is_valid(54, [10]) is False

def test_solve_part_a():
    assert day7.solve_part_a(input_data) == 3749