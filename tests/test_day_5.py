from pathlib import Path
from aoc import day5

day_5_file: Path = Path(__file__).parent / "day5.input"
input_data: str = day5.read_input_file(day_5_file.as_posix())


def test_solve_part_a():
    assert day5.solve_part_a(input_data) == 143


def test_solve_part_b():
    assert day5.solve_part_b(input_data) == 123
