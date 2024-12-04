import typing


def read_lists_from_file(file_path: str) -> typing.Tuple[list[int], list[int]]:
    with open(file_path) as reader:
        lines: list[str] = reader.readlines()
    left, right = list(), list()
    for line in lines:
        l, r = [int(item) for item in line.strip().split()]
        left.append(l)
        right.append(r)
    return left, right


def lists_smallest_distance(left_list: list[int], right_list: list[int]) -> int:
    left_list.sort()
    right_list.sort()
    return sum(abs(l - r) for l, r in zip(left_list, right_list))


def lists_smallest_distance_read_from_file(file_path: str) -> int:
    left_list, right_list = read_lists_from_file(file_path)
    return lists_smallest_distance(left_list, right_list)


def lists_similarity_score(left_list: list[int], right_list: list[int]) -> int:
    similarity_score: int = 0
    for l in left_list:
        l_occurences = [r for r in right_list if r == l]
        similarity_score += l * len(l_occurences)
    return similarity_score
