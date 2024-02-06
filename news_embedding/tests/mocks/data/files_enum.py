from enum import Enum


def get_fullpath(filename: str):
    path_prefix = "./tests/mocks/data"
    return f"{path_prefix}/{filename}"


class MockGraphData(Enum):
    Graph1 = get_fullpath("graph_1.adjlist")
