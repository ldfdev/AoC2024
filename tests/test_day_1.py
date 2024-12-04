from pathlib import Path
from aoc import day1

left_list = [3, 4, 2, 1, 3, 3]
right_list = [4, 3, 5, 3, 9, 3]
day_1_file: Path = Path(__file__).parent / "day1.input"


def test_lists_smallest_distance():
    distance: int = day1.lists_smallest_distance(left_list, right_list)
    assert distance == 11


def test_lists_smallest_distance_read_from_file():
    distance: int = day1.lists_smallest_distance_read_from_file(day_1_file.as_posix())
    assert distance == 11


def test_lists_similarity_score():
    left_list, right_list = day1.read_lists_from_file(day_1_file)
    distance: int = day1.lists_similarity_score(left_list, right_list)
    assert distance == 31
