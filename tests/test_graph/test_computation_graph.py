from graph.computation_graph import convert_dependency_graph_to_computation_graph
from graph.dependency_graph import register_delayed_value_node, register_delayed_caller_node, register_function_call, H
import pytest


@pytest.yield_fixture()
def build_graph():
    H.dependency_graph.clear()
    for i in range(1, 13):
        register_delayed_value_node(i)
    for i in range(101, 105):
        register_delayed_caller_node(i)
    for i, j in zip(range(70, 74), [1, 2, 3, 6]):
        register_delayed_caller_node(i)
        register_function_call({}, i, (j,))
    register_function_call(dict(x=1, y=2, z=3), 101, (4, 5))
    register_function_call(dict(x=6, y=4), 102, (7, 8))
    register_function_call(dict(x=4, y=5), 103, (9, 10))
    register_function_call(dict(x=7, y=8, z=9, w=10), 104, (11, 12))
    yield
    H.dependency_graph.clear()


def test_computation_graph(build_graph):
    G = convert_dependency_graph_to_computation_graph()
    assert sorted(G.nodes()) == [70, 71, 72, 73, 101, 102, 103, 104]
    assert sorted(G.edges()) == sorted([
        (70, 101), (71, 101), (72, 101),
        (73, 102),
        (101, 102),
        (101, 103),
        (103, 104),
        (102, 104),
    ])
