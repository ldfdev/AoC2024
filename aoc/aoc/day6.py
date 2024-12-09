import logging
import typing
import enum
import dataclasses

logger = logging.getLogger(__name__)

Puzzle = list[list[str]]

obstacle = "#"
visited = "X"


class GuardOrientation(enum.Enum):
    UP = "^"
    DOWN = "v"
    RIGHT = ">"
    LEFT = "<"

    @staticmethod
    def orientations() -> list[str]:
        return [e.value for e in GuardOrientation]


@dataclasses.dataclass
class GuardPositionsDetails:
    position: typing.Tuple[int, int]
    orientation: GuardOrientation


def read_input_file(file_path: str) -> Puzzle:
    with open(file_path) as reader:
        return [[letter for letter in line] for line in reader.read().splitlines()]


def identofy_guard_position(puzzle: Puzzle) -> typing.Optional[GuardPositionsDetails]:
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            for o in GuardOrientation:
                if puzzle[row][col] == o.value:
                    return GuardPositionsDetails(
                        position=(
                            row,
                            col,
                        ),
                        orientation=o,
                    )


def identify_next_guard_position(
    puzzle: Puzzle, currnt_position: GuardPositionsDetails
) -> typing.Optional[GuardPositionsDetails]:

    current_row, current_col = currnt_position.position
    orientation: GuardOrientation = currnt_position.orientation
    if orientation == GuardOrientation.UP:
        for i in reversed(range(current_row + 1)):
            if puzzle[i][current_col] == obstacle:
                new_orientation: GuardOrientation = GuardOrientation.RIGHT
                new_row, new_col = i + 1, current_col
                return GuardPositionsDetails(
                    position=(new_row, new_col), orientation=new_orientation
                )
            puzzle[i][current_col] = visited
    elif orientation == GuardOrientation.DOWN:
        for i in range(current_row, len(puzzle)):
            if puzzle[i][current_col] == obstacle:
                new_orientation: GuardOrientation = GuardOrientation.LEFT
                new_row, new_col = i - 1, current_col
                return GuardPositionsDetails(
                    position=(new_row, new_col), orientation=new_orientation
                )
            puzzle[i][current_col] = visited
    elif orientation == GuardOrientation.RIGHT:
        for j in range(current_col, len(puzzle[0])):
            if puzzle[current_row][j] == obstacle:
                new_orientation: GuardOrientation = GuardOrientation.DOWN
                new_row, new_col = current_row, j - 1
                return GuardPositionsDetails(
                    position=(new_row, new_col), orientation=new_orientation
                )
            puzzle[current_row][j] = visited
    elif orientation == GuardOrientation.LEFT:
        for j in reversed(range(current_col + 1)):
            if puzzle[current_row][j] == obstacle:
                new_orientation: GuardOrientation = GuardOrientation.UP
                new_row, new_col = current_row, j + 1
                return GuardPositionsDetails(
                    position=(new_row, new_col), orientation=new_orientation
                )
            puzzle[current_row][j] = visited


def print_puzzle(puzzle: Puzzle):
    puzzle_lines: list[str] = ["".join(line) for line in puzzle]
    pretty_printed_puzzle: str = "\n".join([""] + puzzle_lines)
    logger.info(f"Puzzle: {pretty_printed_puzzle}")

def solve_part_a(puzzle: Puzzle) -> int:
    "counts the positions visited by the patrol guard in the Puzzle"
    gp: GuardPositionsDetails = identofy_guard_position(puzzle)
    logger.info(f"Identified initial guard position {gp}")
    while gp:
        next_gp: typing.Optional[GuardPositionsDetails] = identify_next_guard_position(
            puzzle, gp
        )
        print_puzzle(puzzle)
        gp = next_gp

    return count_visited_cells(puzzle)


def count_visited_cells(puzzle: Puzzle) -> int:
    return sum([len([e for e in line if e == visited]) for line in puzzle])
