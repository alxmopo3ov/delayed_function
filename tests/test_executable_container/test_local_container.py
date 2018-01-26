from executable_container.local_container import LocalContainer
from graph.dependency_graph import dependency_graph_context, register_function_call
from lazy.lazy_caller import LazyCaller
from lazy.lazy_value import get_lazy_value_type
from serialize.serialization_handler import SerializationHandler
import pytest
from numbers import Number


def func1(x, y):
    return x + 1, y + 2


def func2():
    return 2, 5


def func3(x, y):
    pass


@pytest.yield_fixture(params=
[
    (dict(x=Number, y=Number), func1, (Number, Number)),
    ({}, func2, (Number, Number)),
    (dict(x=Number, y=Number), func3, ())
]
)
def lazy_function(request):
    inps, func, outs = request.param

    class X(object):
        def __init__(self):
            self.container_params = None
            self.environment_params = None
            self.func = func
            self.inputs = inps
            self.outputs = outs

    return X()


@pytest.yield_fixture()
def dependency_graph(lazy_function):
    inps = lazy_function.inputs
    outs = lazy_function.outputs
    # here i build dependency graph on my own, without using @lazy_function
    # don't do this on your own!
    with dependency_graph_context("default"):
        inp_dict = {key: get_lazy_value_type(value)() for key, value in inps.items()}
        outs_tuple = tuple(get_lazy_value_type(x)() for x in outs)
        register_function_call(inp_dict, LazyCaller(lazy_function), outs_tuple)
        yield inp_dict, lazy_function, outs_tuple


def test_run_local_container(dependency_graph):
    inputs_dict, func, outputs_tuple = dependency_graph
    outputs_dict = {i: x for i, x in enumerate(outputs_tuple)}

    # containers accept only serialized data
    S = SerializationHandler()
    if len(inputs_dict):
        serialized_evaluated_dict = {
            inputs_dict['x']: S.serialize(1),
            inputs_dict['y']: S.serialize(3)
        }
    else:
        serialized_evaluated_dict = {}

    container = LocalContainer(inputs_dict, func, outputs_dict, serialized_evaluated_dict)
    container.run()

    # containers return only serialized data
    if len(outputs_tuple):
        assert S.deserialize(serialized_evaluated_dict[outputs_tuple[0]], int) == 2
        assert S.deserialize(serialized_evaluated_dict[outputs_tuple[1]], int) == 5
