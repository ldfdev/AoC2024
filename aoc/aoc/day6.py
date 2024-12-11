import logging
import typing
import enum
import dataclasses

logger = logging.getLogger(__name__)

Puzzle = list[list[str]]
Position = typing.Tuple[int, int]

obstacle = "#"
visited = "X"
new_obstruction = "O"


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
    position: Position
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


def advance_position(
    puzzle: Puzzle, currnt_position: GuardPositionsDetails
) -> typing.Optional[Position]:
    """Identifies the next position dictated by curent position and orientation"""
    current_row, current_col = currnt_position.position
    orientation: GuardOrientation = currnt_position.orientation
    new_row, new_col = None, None
    if orientation == GuardOrientation.UP:
        # when moving up, row index decreases by 1
        new_row, new_col = current_row - 1, current_col
        if new_row < 0:
            return
    elif orientation == GuardOrientation.DOWN:
        # when moving down, row index increases by 1
        new_row, new_col = current_row + 1, current_col
        if new_row >= len(puzzle):
            return
    elif orientation == GuardOrientation.RIGHT:
        # when moving right, col index increases by 1
        new_row, new_col = current_row, current_col + 1
        if new_col >= len(puzzle[0]):
            return
    elif orientation == GuardOrientation.LEFT:
        # when moving left, col index decreases by 1
        new_row, new_col = current_row, current_col - 1
        if new_col < 0:
            return
    return (
        new_row,
        new_col,
    )


def identify_next_guard_position(
    puzzle: Puzzle, currnt_position: GuardPositionsDetails
) -> typing.Optional[GuardPositionsDetails]:

    current_row, current_col = currnt_position.position
    current_orientation: GuardOrientation = currnt_position.orientation

    puzzle[current_row][current_col] = visited

    next_position: typing.Optional[Position] = advance_position(puzzle, currnt_position)
    if not next_position:
        return

    next_row, next_col = next_position
    obstacles = [obstacle, new_obstruction]
    if puzzle[next_row][next_col] in obstacles:
        next_orientation: GuardOrientation = GuardOrientation.UP
        if current_orientation == GuardOrientation.UP:
            next_orientation = GuardOrientation.RIGHT
        elif current_orientation == GuardOrientation.RIGHT:
            next_orientation = GuardOrientation.DOWN
        elif current_orientation == GuardOrientation.DOWN:
            next_orientation = GuardOrientation.LEFT
        next_position: typing.Optional[Position] = advance_position(
            puzzle,
            GuardPositionsDetails(
                position=currnt_position.position, orientation=next_orientation
            ),
        )
        if next_position:
            return GuardPositionsDetails(
                position=next_position, orientation=next_orientation
            )
        return

    return GuardPositionsDetails(
        position=next_position, orientation=current_orientation
    )


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


def add_obstruction(
    currnt_position: GuardPositionsDetails, puzzle: Puzzle
) -> typing.Optional[Position]:
    """
    Adds an obstruction in front of the guard, if it is possible
    """
    current_row, current_col = currnt_position.position
    new_row, new_col = None, None
    orientation: GuardOrientation = currnt_position.orientation
    if orientation == GuardOrientation.UP:
        new_row, new_col = current_row - 1, current_col
    elif orientation == GuardOrientation.DOWN:
        new_row, new_col = current_row + 1, current_col
    elif orientation == GuardOrientation.RIGHT:
        new_row, new_col = current_row, current_col + 1
    elif orientation == GuardOrientation.LEFT:
        new_row, new_col = current_row, current_col - 1

    if (new_row < 0) or (new_row >= len(puzzle)):
        return
    if (new_col < 0) or (new_col >= len(puzzle[0])):
        return

    puzzle[new_row][new_col] = new_obstruction
    return (
        new_row,
        new_col,
    )


def remove_obstruction(currnt_position: Position, puzzle: Puzzle, value: str):
    row, col = currnt_position
    puzzle[row][col] = value


def solve_part_b(puzzle: Puzzle) -> int:
    "counts the positions where new obstructions can be placed so that guard moves indefinitely whithout quitting the puzzle"
    gp: GuardPositionsDetails = identofy_guard_position(puzzle)
    logger.info(f"Identified initial guard position {gp}")
    positions_history: dict[Position, GuardOrientation] = dict()

    obstruction_positions: list[Position] = list()
    while gp:
        # import pdb; pdb.set_trace()
        positions_history[gp.position] = gp.orientation
        next_gp: typing.Optional[GuardPositionsDetails] = identify_next_guard_position(
            puzzle, gp
        )
        if not next_gp:
            break
        
        if next_gp.position in positions_history:
            visited_positions: list[GuardOrientation] = [
                positions_history[next_gp.position],
                next_gp.orientation,
            ]
            logger.info(
                f"Identified position {next_gp.position} has already been visited {visited_positions}"
            )

            next_gp_puzzle_value = puzzle[next_gp.position[0]][next_gp.position[1]]
            obstruction_position: typing.Optional[Position] = add_obstruction(
                next_gp, puzzle
            )
            if not obstruction_position:
                break
            print_puzzle(puzzle)
            next_next_gp: typing.Optional[GuardPositionsDetails] = (
                identify_next_guard_position(
                    puzzle, identify_next_guard_position(puzzle, next_gp)
                )
            )
            if next_next_gp and (next_next_gp.position in positions_history):
                if next_next_gp.orientation == positions_history[next_next_gp.position]:
                    logger.info(
                        f"Detected new obstruction position at {obstruction_position}"
                    )
                    obstruction_positions.append(obstruction_position)
                    print_puzzle(puzzle)
            remove_obstruction(obstruction_position, puzzle, next_gp_puzzle_value)
        gp = next_gp

    return len(obstruction_positions)


def count_visited_cells(puzzle: Puzzle) -> int:
    return sum([len([e for e in line if e == visited]) for line in puzzle])
