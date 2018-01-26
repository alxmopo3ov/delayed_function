from utils.marked_graph import create_marked_graph
import pytest
import networkx as nx
import numpy as np


@pytest.yield_fixture()
def complex_graph():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 101, 102, 103, 104, 105, 106, 70, 71, 72, 73])
    G.add_edges_from(
        [(1, 101), (2, 101), (3, 101), (4, 102), (4, 103), (5, 103), (6, 102), (7, 104), (7, 105), (7, 106), (8, 104),
         (8, 105), (8, 106), (9, 104), (9, 105), (9, 106), (10, 104), (10, 105), (10, 106), (101, 4), (101, 5),
         (102, 7), (102, 8), (103, 9), (103, 10), (104, 11), (104, 12), (70, 1), (71, 2), (72, 3), (73, 6)]
    )
    yield G


def normalize_dict(dct):
    res = {}
    for key, value in dct.items():
        res[np.round(key, 2)] = tuple(np.round(x, 2) for x in value)


def test_marks(complex_graph):
    _, pos = create_marked_graph(complex_graph)
    pos = {int(repr(key)): value for key, value in pos.items()}
    assert normalize_dict(pos) == normalize_dict({
        1: (0.6, 6),
        2: (1.2, 6),
        3: (1.8, 6),
        4: (1.0, 4),
        5: (2.0, 4),
        6: (2.4, 6),
        7: (0.6, 2),
        8: (1.2, 2),
        9: (1.8, 2),
        10: (2.4, 2),
        11: (1.0, 0),
        12: (2.0, 0),
        101: (1.5, 5),
        102: (1.0, 3),
        103: (2.0, 3),
        104: (0.75, 1),
        105: (1.5, 1),
        106: (2.25, 1),
        70: (0.6, 7),
        71: (1.2, 7),
        72: (1.8, 7),
        73: (2.4, 7)
    })
