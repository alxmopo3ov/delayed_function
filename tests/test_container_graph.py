from graph.container_graph import convert_dependency_graph_to_container_graph
from graph.dependency_graph import register_lazy_value_node, register_lazy_caller_node, register_function_call, \
    dependency_graph
import pytest
import networkx as nx


class ValueTypedNode(object):
    value_type = int

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return self.value_type.__name__ + " " + str(self.x)


@pytest.yield_fixture()
def build_graph():
    dependency_graph.clear()
    nodes = {}
    caller_nodes = [101, 102, 103, 70, 104, 105, 106, 71, 73, 72]
    for i in range(1, 13):
        cur_node = ValueTypedNode(i)
        nodes[i] = cur_node
        register_lazy_value_node(cur_node)
    for i in range(101, 107):
        register_lazy_caller_node(i)
    for i, j in zip(range(70, 74), [1, 2, 3, 6]):
        register_lazy_caller_node(i)
        register_function_call({}, i, (nodes[j],))
    register_function_call(dict(x=nodes[1], y=nodes[2], z=nodes[3]), 101, (nodes[4], nodes[5]))
    register_function_call(dict(x=nodes[6], y=nodes[4]), 102, (nodes[7], nodes[8]))
    register_function_call(dict(x=nodes[4], y=nodes[5]), 103, (nodes[9], nodes[10]))
    register_function_call(dict(x=nodes[7], y=nodes[8], z=nodes[9], w=nodes[10]), 104, (nodes[11], nodes[12]))
    for i in range(1, 3):
        register_function_call(dict(x=nodes[7], y=nodes[8], z=nodes[9], w=nodes[10]), 104 + i, ())

    yield nodes, caller_nodes
