from aoc import day11
from pathlib import Path

day_11_file: Path = Path(__file__).parent / "day11.input"
input_data: list[int] = day11.read_input_file(day_11_file.as_posix())


def test_stone_evolution():
    assert day11.stone_evolution(0) == [1]
    assert day11.stone_evolution(10) == [1, 0]
    assert day11.stone_evolution(123009) == [123, 9]
    assert day11.stone_evolution(221) == [221 * 2024]


def test_blink():
    stones = input_data
    assert day11.blink(stones) == [253000, 1, 7]

    stones = [253000, 1, 7]
    assert day11.blink(stones) == [253, 0, 2024, 14168]

    stones = [253, 0, 2024, 14168]
    assert day11.blink(stones) == [512072, 1, 20, 24, 28676032]

    stones = [512072, 1, 20, 24, 28676032]
    assert day11.blink(stones) == [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]

    stones = [512, 72, 2024, 2, 0, 2, 4, 2867, 6032]
    assert day11.blink(stones) == [
        1036288,
        7,
        2,
        20,
        24,
        4048,
        1,
        4048,
        8096,
        28,
        67,
        60,
        32,
    ]

    stones = [1036288, 7, 2, 20, 24, 4048, 1, 4048, 8096, 28, 67, 60, 32]
    assert day11.blink(stones) == [
        2097446912,
        14168,
        4048,
        2,
        0,
        2,
        4,
        40,
        48,
        2024,
        40,
        48,
        80,
        96,
        2,
        8,
        6,
        7,
        6,
        0,
        3,
        2,
    ]


def test_solve_part_a():
    assert day11.solve_part_a(input_data) == 55312


def test_solve_part_b():
    assert day11.solve_part_b(input_data) == 55312
