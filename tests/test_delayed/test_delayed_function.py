from delayed.delayed_function import delayed_function, build_dependency_graph, DelayedFlagsHandler
from delayed.delayed_value import get_delayed_value_type
from serialize.initialized_value_storage import initialized_value_storage
from graph.dependency_graph import H
from numbers import Number
import inspect
import networkx as nx


def test_build_dependency_graph():
    assert not DelayedFlagsHandler.DELAYED_ENABLED
    with build_dependency_graph("test_graph"):
        assert DelayedFlagsHandler.DELAYED_ENABLED
        assert H.dependency_graph.dependency_graph_id == "test_graph"
    assert not DelayedFlagsHandler.DELAYED_ENABLED


def test_evaluate_disabled_delayed():
    @delayed_function(outputs=(Number, Number, Number), inputs=dict(x=Number, y=Number, z=Number))
    def func(x, y, z=3.4):
        return x + 1, y + 2, z + 3

    assert func(1, 2) == (2, 4, 6.4)


def test_evaluate_enabled_delayed():
    DelayedFlagsHandler.DELAYED_ENABLED = True

    @delayed_function(outputs=(Number, Number, Number), inputs=dict(x=Number, y=Number, z=Number))
    def func(x, y, z=3.4):
        return x + 1, y + 2, z + 3

    x, y, z = func(1, 2)
    assert all(isinstance(s, get_delayed_value_type(Number)) for s in (x, y, z))
    assert sorted(initialized_value_storage.values()) == [1, 2, 3.4]


def test_delayed_function_has_necessary_attrs():
    @delayed_function(outputs=(Number, Number, Number), inputs=dict(x=Number, y=Number, z=Number))
    def func(x, y, z=3.4):
        return x + 1, y + 2, z + 3

    assert func.inputs == dict(x=Number, y=Number, z=Number)
    assert func.outputs == (Number, Number, Number)
    assert func.func == inspect.unwrap(func)


# TODO: make more conscious testing
def test_delayed_function_build_graph():
    @delayed_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def add(x, y):
        return x + 1, y + 1

    @delayed_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def mul(x, y):
        return x * 10, y * 10

    @delayed_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def div(x, y):
        return x / 2, y / 2

    @delayed_function(outputs=(), inputs=dict(x=Number, y=Number, z=Number, w=Number))
    def print_nums(x, y, z, w):
        print(x, y, z, w)

    with build_dependency_graph("default"):
        a, b = add(1, 2)
        c, d = mul(3, 4)
        e, f = div(b, c)
        print_nums(*(mul(a, e) + add(f, d)))

    H.dependency_graph.validate()
