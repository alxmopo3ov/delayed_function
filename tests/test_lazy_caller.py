from lazy.lazy_caller import LazyCaller, generate_lazy_function_call
from graph.dependency_graph import dependency_graph
import pytest


@pytest.yield_fixture()
def clear_graph():
    dependency_graph.clear()
    yield
    dependency_graph.clear()


def test_lazy_caller(clear_graph):
    def f():
        return 1
    caller = LazyCaller(f)
    assert caller.func == f
    assert caller.func() == 1
    assert caller in dependency_graph
    assert caller in dependency_graph.lazy_callers
    assert repr(caller) == "LazyCaller[f]"  # because func.__name__ = f
    assert caller.caller_id == 0


def test_generate_lazy_caller(clear_graph):
    def f():
        return 1
    caller = generate_lazy_function_call(f)
    assert caller.func == f
    assert caller.func() == 1
    assert caller in dependency_graph
    assert caller in dependency_graph.lazy_callers
    assert repr(caller) == "LazyCaller[f]"  # because func.__name__ = f
    assert caller.caller_id == 0
