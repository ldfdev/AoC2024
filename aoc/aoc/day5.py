from collections import defaultdict
import logging
import typing

logger = logging.getLogger(__name__)


class Graph:
    def __init__(self):
        self.adjacencies: dict[int, list[int]] = defaultdict(list)

    def add_edge(self, from_, to_):
        if from_ not in self.adjacencies:
            self.adjacencies[from_] = list()
        self.adjacencies[from_].append(to_)

    def is_dest_reachable_from_src(self, src, dest) -> bool:
        """
        DFS to determine if node dest is reachable from src
        """
        prev = dict()
        visited = set()
        stack = [src]
        while len(stack) > 0:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            neighbors = self.adjacencies[current]
            if dest in neighbors:
                prev[dest] = current
                self.show_path(src, dest, prev)
                return True
            stack.extend(neighbors)
            for n in neighbors:
                prev[n] = current
        return False

    def are_edges_dirrcetly_conencted(self, source, dest) -> bool:
        return dest in self.adjacencies[source]

    def show_path(Self, src, dest, paths_dict):
        paths = [dest]
        while paths[-1] != src:
            paths.append(paths_dict[paths[-1]])
        paths = list(reversed(paths))
        logger.info(f"Node {src} -> {dest} is reachable via {paths}")


def build_graph(input_data: str) -> Graph:
    relationships: Graph = Graph()
    lines = input_data.strip().split("\n")
    for line in lines:
        if "|" not in line:
            break
        prev_, next_ = [int(x) for x in line.split("|")]
        relationships.add_edge(prev_, next_)
    return relationships


def build_update_list(input_data: str) -> list[list[int]]:
    lines = input_data.strip().split("\n")
    update_list: list[list[int]] = list()
    for line in lines:
        if "," not in line:
            continue
        update_list.append([int(x) for x in line.split(",")])
    return update_list


def get_pairs_from_update_list(
    update_list: list[list[int]],
) -> list[list[int]]:
    """
    if update list is a_1, a_2, a_3
    we obtain all pairs: (a_2, a_1), (a_3, a_2), (a_3, a_1)
    """
    relationships: list[list[int]] = list()
    for i in range(len(update_list)):
        for j in range(i + 1, len(update_list)):
            relationships.append([update_list[j], update_list[i]])
    return relationships


def is_update_list_correct(graph: Graph, update_list: list[int]) -> bool:
    """
    FOr an update list a1, a2, an
    it is not correct if node a(i) is reachable from node a(i + k)
    """
    update_list_pairs: list[list[int]] = get_pairs_from_update_list(update_list)
    for source, dest in update_list_pairs:
        # if graph.is_dest_reachable_from_src(source, dest):
        if graph.are_edges_dirrcetly_conencted(source, dest):
            return False
    return True


def solve_part_a(input_data: str) -> int:
    graph: Graph = build_graph(input_data)
    update_lists: list[list[int]] = build_update_list(input_data)

    middle_elements_sum = 0
    for num, update_list in enumerate(update_lists, start=1):
        if not is_update_list_correct(graph, update_list):
            logger.warning(f"Update list {num}:{update_list} is not correct")
            continue
        middle = update_list[len(update_list) // 2]
        middle_elements_sum += middle

    return middle_elements_sum


def reorder_update_List(graph: Graph, update_list_: list[int]) -> list[int]:
    update_list: list[int] = [i for i in update_list_]
    rules: list[typing.Tuple[int, int]] = list()
    for k, values in graph.adjacencies.items():
        for v in values:
            if (k in update_list) and (v in update_list):
                rules.append(
                    (
                        k,
                        v,
                    )
                )
    logger.info(f"Rules {rules}")
    for i in range(len(update_list)):
        for j in range(i + 1, len(update_list)):
            reversed_rule = (update_list[j], update_list[i])
            if reversed_rule in rules:
                temp = update_list[i]
                update_list[i] = update_list[j]
                update_list[j] = temp
    logger.info(f"New update list {update_list}")
    return update_list


def solve_part_b(input_data: str) -> int:
    graph: Graph = build_graph(input_data)
    update_lists: list[list[int]] = build_update_list(input_data)

    middle_elements_sum = 0
    for num, update_list in enumerate(update_lists, start=1):
        if is_update_list_correct(graph, update_list):
            continue
        logger.warning(f"Update list {num}:{update_list} is not correct")
        update_list = reorder_update_List(graph, update_list)
        assert is_update_list_correct(graph, update_list)
        middle = update_list[len(update_list) // 2]
        middle_elements_sum += middle

    return middle_elements_sum


def read_input_file(file_path: str) -> str:
    with open(file_path) as reader:
        return reader.read()
