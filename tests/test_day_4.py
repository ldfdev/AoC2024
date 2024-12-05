from pathlib import Path
from aoc import day4
from unittest.mock import patch

day_4_file: Path = Path(__file__).parent / "day4.input"
puzzle: day4.Puzzle = day4.read_puzzle_from_file(day_4_file.as_posix())


def test_line_count():
    line = "MMMSXXMASM"
    assert day4.line_count(line) == 1

    line = "MMAMSXMASM"
    assert day4.line_count(line) == 1


def test_extract_vertical_lines():
    with patch("aoc.day4.extract_horizontal_lines") as mock_extract_vertical_lines:
        mock_extract_vertical_lines.return_value = ["XMAS", "XMAS"]
        vertical_lines: list[str] = day4.extract_vertical_lines(puzzle)
        assert vertical_lines == ["XX", "MM", "AA", "SS"]


def test_extract_diagonal_lines():
    with patch("aoc.day4.extract_horizontal_lines") as mock_extract_vertical_lines:
        mock_extract_vertical_lines.return_value = ["XMAS", "XMAS", "XMAS", "XMAS"]
        diagonal_lines: list[str] = day4.extract_diagonal_lines(puzzle)
        assert diagonal_lines == ["XMAS", "SAMX"]


def test_count_xmas_in_puzzle():
    assert day4.count_xmas_in_puzzle(puzzle) == 18


def test_count_x_mas():
    assert day4.count_x_mas(puzzle) == 9
