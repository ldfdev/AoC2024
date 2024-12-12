import itertools
from collections import Counter, defaultdict


def read_input_file(file_Path: str) -> list[int]:
    with open(file_Path) as reader:
        stones: list[str] = reader.read().strip().split()
    return [int(s) for s in stones]


def stone_evolution(stone: int) -> list[int]:
    """
    defines how a stone is changed based on the rules in the problem statement
    """
    if stone == 0:
        return [1]
    str_stone = str(stone)
    if len(str_stone) % 2 == 0:
        middle = len(str_stone) // 2
        first, second = str_stone[:middle], str_stone[middle:]
        return [int(first), int(second)]
    return [stone * 2024]


def blink(stones: list[int]) -> list[int]:
    return list(itertools.chain(*[stone_evolution(stone) for stone in stones]))


def solve_part_a(stones: list[int]) -> int:
    """count the number of stone after blinking 25 times"""
    initial: list[int] = [stone for stone in stones]
    for _ in range(25):
        initial = blink(initial)
    return len(initial)


def solve_part_b(stones: list[int]) -> int:
    """count the number of stone after blinking 25 times"""
    initial: dict[int, int] = Counter(stones)
    for _ in range(75):
        new_counter = defaultdict(int)
        for stone in initial:
            new_stones: list[int] = stone_evolution(stone)
            for new_stone in new_stones:
                new_counter[new_stone] += initial[stone]
        initial = new_counter
    return sum(initial.values())
