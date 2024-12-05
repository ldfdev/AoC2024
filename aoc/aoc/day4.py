import logging
from rich import print

logger = logging.getLogger(__name__)

Puzzle = str


def read_puzzle_from_file(file_path: str) -> Puzzle:
    with open(file_path) as reader:
        return reader.read()


def line_count(line: str) -> int:
    word = "XMAS"
    count = 0
    matched_positions: list[int] = list()

    for i in range(0, len(line)):
        sliding_window = line[i : i + 4]
        if (word == sliding_window) or list(reversed(word)) == list(sliding_window):
            count += 1
            matched_positions.append(i)
    if matched_positions:
        print(f"Line {line}")
        for m in matched_positions:
            print(
                f" > {line[:m]}"
                + f"[bold blue]{line[m: m + 4]}[/bold blue]"
                + f"{line[m + 4:]}"
            )
    return count


def extract_horizontal_lines(puzzle: Puzzle) -> list[str]:
    return puzzle.strip().split("\n")


def extract_vertical_lines(puzzle: Puzzle) -> list[str]:
    lines: list[str] = extract_horizontal_lines(puzzle)
    vertical_lines: list[str] = list()
    for column in range(len(lines[0])):
        vertical_line: list[str] = list()
        for i in range(len(lines)):
            vertical_line.append(lines[i][column])
        vertical_lines.append("".join(vertical_line))
    return vertical_lines


def extract_diagonal_lines(puzzle: Puzzle) -> list[str]:
    lines: list[str] = extract_horizontal_lines(puzzle)
    diagonal_first_element = [[i, 0] for i in reversed(range(len(lines)))] + [
        [0, i] for i in range(1, len(lines[0]))
    ]

    diagonal_lines: list[str] = list()

    ## main diagonals
    for l, c in diagonal_first_element:
        diagonal: list[str] = list()
        while l < len(lines) and c < len(lines[0]):
            diagonal.append(lines[l][c])
            l += 1
            c += 1
        # import pdb; pdb.set_trace()
        if len(diagonal) >= 4:
            diagonal_lines.append("".join(diagonal))

    # other diagonals
    diagonal_first_element = [
        [i, len(lines[0]) - 1] for i in range(len(lines) - 1, -1, -1)
    ] + [[0, i] for i in range(0, len(lines[0]) - 1)]
    for l, c in diagonal_first_element:
        diagonal: list[str] = list()
        while (l < len(lines)) and (c > -1):
            diagonal.append(lines[l][c])
            l += 1
            c -= 1
        if len(diagonal) >= 4:
            diagonal_lines.append("".join(diagonal))
    return diagonal_lines


def count_xmas_in_puzzle(puzzle: Puzzle) -> int:
    def count_lines(lines):
        return sum(line_count(line) for line in lines)

    horizontal_lines: list[str] = extract_horizontal_lines(puzzle)
    logger.info(f"The puzzle contains {len(horizontal_lines)} lines")
    horizontal_lines_count: int = count_lines(horizontal_lines)
    logger.info(f"horizontal lines XMAS count: {horizontal_lines_count}")

    vertical_lines: list[str] = extract_vertical_lines(puzzle)
    vertical_lines_count: int = count_lines(vertical_lines)
    logger.info(f"vertical lines XMAS count: {vertical_lines_count}")

    diagonal_lines: list[str] = extract_diagonal_lines(puzzle)
    diagonal_lines_count: int = count_lines(diagonal_lines)
    logger.info(f"diagonal lines XMAS count: {diagonal_lines_count}")

    return horizontal_lines_count + vertical_lines_count + diagonal_lines_count


def count_x_mas(puzzle: Puzzle) -> int:
    def is_slice_an_x_mas(slice) -> bool:
        printable_slice = "\n > ".join([""] + slice)
        logger.info(f"Verifying slice {printable_slice}")
        word = "MAS"
        lines = [
            "".join([slice[0][0], slice[1][1], slice[2][2]]),
            "".join([slice[2][0], slice[1][1], slice[0][2]]),
        ]
        allowed = [word, "".join(reversed(word))]
        for line in lines:
            if line not in allowed:
                return False
        return True

    count = 0
    lines = extract_horizontal_lines(puzzle)
    for i in range(len(lines)):
        if i + 2 >= len(lines):
            break
        for j in range(len(lines[0])):
            if j + 2 >= len(lines[0]):
                break
            slice = [
                lines[i][j : j + 3],
                lines[i + 1][j : j + 3],
                lines[i + 2][j : j + 3],
            ]
            if is_slice_an_x_mas(slice):
                count += 1
    return count
