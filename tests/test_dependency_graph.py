from graph.dependency_graph import H, register_lazy_value_node, \
    register_function_call, register_lazy_caller_node
import pytest


@pytest.yield_fixture()
def dependency_graph():
    H.dependency_graph.clear()
    yield H.dependency_graph
    H.dependency_graph.clear()


def test_clear(dependency_graph):
    register_lazy_caller_node(1)
    register_lazy_value_node(2)
    dependency_graph.clear()
    assert 1 not in dependency_graph
    assert 1 not in dependency_graph.lazy_callers
    assert 2 not in dependency_graph
    assert 2 not in dependency_graph.lazy_values
    assert register_lazy_caller_node(1) == 0


def test_register_lazy_value(dependency_graph):
    register_lazy_value_node(1)
    assert 1 in dependency_graph.lazy_values
    assert 1 in dependency_graph.nodes()


def test_register_lazy_caller(dependency_graph):
    res = register_lazy_caller_node(1)
    assert 1 in dependency_graph.lazy_callers
    assert 1 in dependency_graph.nodes()
    assert res == 0


def test_register_multiple_callers(dependency_graph):
    res1 = register_lazy_caller_node(1)
    res2 = register_lazy_caller_node(2)
    res3 = register_lazy_caller_node(3)
    assert 1 in dependency_graph.lazy_callers
    assert 2 in dependency_graph.lazy_callers
    assert 3 in dependency_graph.lazy_callers
    assert 1 in dependency_graph.nodes()
    assert 2 in dependency_graph.nodes()
    assert 3 in dependency_graph.nodes()
    assert res1 == 0
    assert res2 == 1
    assert res3 == 2


def test_register_function_call(dependency_graph):
    inputs = dict(x=1, y=2, z=3)
    outputs = (4, 5)
    for x in tuple(inputs.values()) + outputs:
        register_lazy_value_node(x)
    caller = 74
    register_lazy_caller_node(caller)
    register_function_call(inputs, caller, outputs)
    assert sorted(dependency_graph.edges(data=True)) == sorted(
        [
            (1, caller, {'input_name': 'x'}),
            (2, caller, {'input_name': 'y'}),
            (3, caller, {'input_name': 'z'}),
            (caller, 4, {'output_id': 0}),
            (caller, 5, {'output_id': 1})
        ]
    )


def test_empty_graph_validation(dependency_graph):
    dependency_graph.validate()


def test_wrong_call_graph_validation(dependency_graph):
    register_lazy_caller_node(1)
    register_lazy_caller_node(2)
    dependency_graph.add_edge(1, 2)
    with pytest.raises(AssertionError):
        dependency_graph.validate()


def test_wrong_value_graph_validation(dependency_graph):
    register_lazy_value_node(1)
    register_lazy_value_node(2)
    dependency_graph.add_edge(1, 2)
    with pytest.raises(AssertionError):
        dependency_graph.validate()
