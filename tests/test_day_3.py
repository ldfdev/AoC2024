from pathlib import Path
from aoc import day3

day_3_file: Path = Path(__file__).parent / "day3.input"


def test_extract_multiplication_instructions():
    instruction: day3.Instructions = "xmul(2,4)%&mul[3,7]!@^do_"
    result: list[day3.MultiplicationInstruction] = (
        day3.extract_multiplication_instructions(instruction)
    )
    assert len(result) == 1, f"Not found list with 1 item: {result}"
    mi: day3.MultiplicationInstruction = result[0]
    assert mi.operands == [2, 4]

    instruction: day3.Instructions = "xmul(2@,4)%&mul[3,7]!@^do_"
    result: list[day3.MultiplicationInstruction] = (
        day3.extract_multiplication_instructions(instruction)
    )
    assert result == list()

    instruction: day3.Instructions = "xmul(2@<>4%&mul[37]!@^do)_"
    result: list[day3.MultiplicationInstruction] = (
        day3.extract_multiplication_instructions(instruction)
    )
    assert result == list()


def test_execute_instructions():
    instructions: day3.Instructions = day3.read_instructions_from_file(day_3_file)
    assert day3.execute_instructions(instructions) == 161


def test_extract_do_instructions():
    instructions = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    lst: list[day3.EnableMultiplicationInstruction] = day3.extract_do_instructions(
        instructions
    )
    assert len(lst) == 1


def test_extract_dont_instructions():
    instructions = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    lst: list[day3.DisableMultiplicationInstruction] = day3.extract_dont_instructions(
        instructions
    )
    assert len(lst) == 1


def test_combine_instructions():
    instructions = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    parsed: list[day3.ParsedInstruction] = day3.combine_instructions(instructions)
    assert len(parsed) == 6
    assert isinstance(parsed[0], day3.MultiplicationInstruction)
    assert parsed[0].operands == [2, 4]

    assert isinstance(parsed[1], day3.DisableMultiplicationInstruction)

    assert isinstance(parsed[2], day3.MultiplicationInstruction)
    assert parsed[2].operands == [5, 5]

    assert isinstance(parsed[3], day3.MultiplicationInstruction)
    assert parsed[3].operands == [11, 8]

    assert isinstance(parsed[4], day3.EnableMultiplicationInstruction)

    assert isinstance(parsed[5], day3.MultiplicationInstruction)
    assert parsed[5].operands == [8, 5]


def test_execute_instructions_with_enable_capabilities():
    instructions: day3.Instructions = day3.read_instructions_from_file(day_3_file)

    assert day3.execute_instructions_with_enable_capabilities(instructions) == 48
