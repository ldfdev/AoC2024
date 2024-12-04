import collections
import operator
import typing

Instructions = str


class ParsedInstruction:
    def __init__(self, index: int, text: str):
        self.index = index
        self.text = text

    def execute(self) -> int:
        raise NotImplementedError()


class MultiplicationInstruction(ParsedInstruction):
    def __init__(self, index, text, operands: list[int]):
        super().__init__(index, text)
        self.operands = operands

    def execute(self):
        return operator.mul(*self.operands)


class EnableMultiplicationInstruction(ParsedInstruction):
    def __init__(self, index, text):
        super().__init__(index, text)


class DisableMultiplicationInstruction(ParsedInstruction):
    def __init__(self, index, text):
        super().__init__(index, text)


def extract_instruction_by_delimiter(
    instructions: Instructions, start_ins, stop_ins, start=0
) -> typing.Optional[ParsedInstruction]:
    start_pos: int = instructions.find(start_ins, start)
    if start_pos == -1:
        return
    # print(instructions, start_ins, stop_ins, start)
    # import pdb; pdb.set_trace()
    end_pos = instructions.find(stop_ins, start_pos + len(start_ins))
    if end_pos != -1:
        instruction_to_parse = instructions[start_pos + len(start_ins) : end_pos]
        return ParsedInstruction(
            index=start_pos + len(start_ins), text=instruction_to_parse
        )


def extract_instructions_by_delimiter(
    instructions: Instructions, start_ins, stop_ins, start=0
) -> list[ParsedInstruction]:
    pi: typing.Optional[ParsedInstruction] = extract_instruction_by_delimiter(
        instructions, start_ins, stop_ins, start
    )
    result: list[ParsedInstruction] = list()
    while pi:
        result.append(pi)
        pi = extract_instruction_by_delimiter(
            instructions, start_ins, stop_ins, start=pi.index
        )
    return result


def parse_multiplication_instruction(
    instruction: ParsedInstruction,
) -> typing.Optional[MultiplicationInstruction]:
    try:
        instruction_to_parse = instruction.text
        operand1, operand2 = instruction_to_parse.strip().split(",")
        operand1 = int(operand1)
        operand2 = int(operand2)
        return MultiplicationInstruction(
            index=instruction.index,
            text=instruction.text,
            operands=[operand1, operand2],
        )
    except ValueError:
        pass


def parse_do_instruction(
    instruction: ParsedInstruction,
) -> EnableMultiplicationInstruction:
    return EnableMultiplicationInstruction(**instruction.__dict__)


def parse_dont_instruction(
    instruction: ParsedInstruction,
) -> DisableMultiplicationInstruction:
    return DisableMultiplicationInstruction(**instruction.__dict__)


def extract_multiplication_instructions(
    instructions: Instructions,
) -> list[MultiplicationInstruction]:
    start_ins = "mul("
    stop_ins = ")"
    parsed_instructions: list[ParsedInstruction] = extract_instructions_by_delimiter(
        instructions, start_ins=start_ins, stop_ins=stop_ins
    )
    result: list[MultiplicationInstruction] = list(
        filter(
            None,
            (
                parse_multiplication_instruction(parsed_instruction)
                for parsed_instruction in parsed_instructions
            ),
        )
    )
    return result


def extract_do_instructions(
    instructions: Instructions,
) -> list[EnableMultiplicationInstruction]:
    start_ins = "do("
    stop_ins = ")"
    parsed_instructions: list[ParsedInstruction] = extract_instructions_by_delimiter(
        instructions, start_ins=start_ins, stop_ins=stop_ins
    )
    result: list[EnableMultiplicationInstruction] = [
        parse_do_instruction(parsed_instruction)
        for parsed_instruction in parsed_instructions
    ]
    return result


def extract_dont_instructions(
    instructions: Instructions,
) -> list[DisableMultiplicationInstruction]:
    start_ins = "don't("
    stop_ins = ")"
    parsed_instructions: list[ParsedInstruction] = extract_instructions_by_delimiter(
        instructions, start_ins=start_ins, stop_ins=stop_ins
    )
    result: list[DisableMultiplicationInstruction] = [
        parse_dont_instruction(parsed_instruction)
        for parsed_instruction in parsed_instructions
    ]
    return result


def execute_instructions(instructions: Instructions) -> int:
    valid_instructions: list[MultiplicationInstruction] = (
        extract_multiplication_instructions(instructions)
    )
    return sum(operator.mul(*i.operands) for i in valid_instructions)


def combine_instructions(instructions: Instructions) -> list[ParsedInstruction]:
    mi: list[MultiplicationInstruction] = extract_multiplication_instructions(
        instructions
    )
    ei: list[EnableMultiplicationInstruction] = extract_do_instructions(instructions)
    di: list[DisableMultiplicationInstruction] = extract_dont_instructions(instructions)
    combined_instructions: list[ParsedInstruction] = list()
    combined_instructions.extend(mi)
    combined_instructions.extend(ei)
    combined_instructions.extend(di)
    combined_instructions.sort(key=operator.attrgetter("index"))
    return combined_instructions


def execute_instructions_with_enable_capabilities(instructions: Instructions) -> int:
    combined_instructions: list[ParsedInstruction] = combine_instructions(instructions)
    valid_instructions: list[MultiplicationInstruction] = list()
    is_enabled = True
    for i in combined_instructions:
        if isinstance(i, EnableMultiplicationInstruction):
            is_enabled = True
        elif isinstance(i, DisableMultiplicationInstruction):
            is_enabled = False
        elif is_enabled:
            valid_instructions.append(i)

    return sum(operator.mul(*i.operands) for i in valid_instructions)


def read_instructions_from_file(file_path: str) -> Instructions:
    with open(file_path) as reader:
        return reader.read()
