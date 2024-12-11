from pathlib import Path
from aoc import day6

day_6_file: Path = Path(__file__).parent / "day6.input"
input_data: day6.Puzzle = day6.read_input_file(day_6_file.as_posix())


def test_solve_part_a():
    assert day6.solve_part_a(input_data) == 41


def test_solve_part_b():
    assert day6.solve_part_b(input_data) == 6
