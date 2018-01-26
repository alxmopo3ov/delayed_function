from lazy.lazy_caller import LazyCaller, generate_lazy_function_call
from graph.dependency_graph import H
import pytest


@pytest.yield_fixture()
def dependency_graph():
    H.dependency_graph.clear()
    yield H.dependency_graph
    H.dependency_graph.clear()


def test_lazy_caller(dependency_graph):
    def f():
        return 1
    caller = LazyCaller(f)
    assert caller.func == f
    assert caller.func() == 1
    assert caller in dependency_graph
    assert caller in dependency_graph.lazy_callers
    assert repr(caller) == "LazyCaller[f]"  # because func.__name__ = f
    assert caller.caller_id == 0


def test_generate_lazy_caller(dependency_graph):
    def f():
        return 1
    caller = generate_lazy_function_call(f)
    assert caller.func == f
    assert caller.func() == 1
    assert caller in dependency_graph
    assert caller in dependency_graph.lazy_callers
    assert repr(caller) == "LazyCaller[f]"  # because func.__name__ = f
    assert caller.caller_id == 0
