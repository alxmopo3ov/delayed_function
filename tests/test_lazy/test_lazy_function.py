from lazy.lazy_function import lazy_function, build_dependency_graph, LazyFlagsHandler
from lazy.lazy_value import get_lazy_value_type
from serialize.initialized_value_storage import initialized_value_storage
from graph.dependency_graph import H
from numbers import Number
import inspect
import networkx as nx


def test_build_dependency_graph():
    assert not LazyFlagsHandler.LAZY_ENABLED
    with build_dependency_graph("test_graph"):
        assert LazyFlagsHandler.LAZY_ENABLED
        assert H.dependency_graph.dependency_graph_id == "test_graph"
    assert not LazyFlagsHandler.LAZY_ENABLED


def test_evaluate_disabled_lazy():
    @lazy_function(outputs=(Number, Number, Number), inputs=dict(x=Number, y=Number, z=Number))
    def func(x, y, z=3.4):
        return x + 1, y + 2, z + 3

    assert func(1, 2) == (2, 4, 6.4)


def test_evaluate_enabled_lazy():
    LazyFlagsHandler.LAZY_ENABLED = True

    @lazy_function(outputs=(Number, Number, Number), inputs=dict(x=Number, y=Number, z=Number))
    def func(x, y, z=3.4):
        return x + 1, y + 2, z + 3

    x, y, z = func(1, 2)
    assert all(isinstance(s, get_lazy_value_type(Number)) for s in (x, y, z))
    assert sorted(initialized_value_storage.values()) == [1, 2, 3.4]


def test_lazy_function_has_necessary_attrs():
    @lazy_function(outputs=(Number, Number, Number), inputs=dict(x=Number, y=Number, z=Number))
    def func(x, y, z=3.4):
        return x + 1, y + 2, z + 3

    assert hasattr(func, 'container_params')
    assert hasattr(func, 'environment_params')
    assert func.inputs == dict(x=Number, y=Number, z=Number)
    assert func.outputs == (Number, Number, Number)
    assert func.func == inspect.unwrap(func)


# TODO: make more conscious testing
def test_lazy_function_build_graph():
    @lazy_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def add(x, y):
        return x + 1, y + 1

    @lazy_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def mul(x, y):
        return x * 10, y * 10

    @lazy_function(outputs=(Number, Number), inputs=dict(x=Number, y=Number))
    def div(x, y):
        return x / 2, y / 2

    @lazy_function(outputs=(), inputs=dict(x=Number, y=Number, z=Number, w=Number))
    def print_nums(x, y, z, w):
        print(x, y, z, w)

    with build_dependency_graph("default"):
        a, b = add(1, 2)
        c, d = mul(3, 4)
        e, f = div(b, c)
        print_nums(*(mul(a, e) + add(f, d)))

    H.dependency_graph.validate()
