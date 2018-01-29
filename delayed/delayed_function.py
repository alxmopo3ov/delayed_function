import functools
import inspect
import contextlib
from copy import deepcopy
from delayed.delayed_value import get_delayed_value_type, generate_delayed_inputs, generate_delayed_outputs, \
    DelayedCollectionBase, DelayedDictBase, DelayedListBase
from delayed.delayed_caller import generate_delayed_function_call
from delayed.delayed_utils import check_all_are_types, validate_function, convert_to_python_return
from graph.dependency_graph import register_function_call, dependency_graph_context
from utils.type_check import do_type_check


class DelayedFlagsHandler(object):
    DELAYED_ENABLED = False  # by default, our function does not behave as their delayed variants


@contextlib.contextmanager
def build_dependency_graph(dependency_graph_id):
    DelayedFlagsHandler.DELAYED_ENABLED = True
    with dependency_graph_context(dependency_graph_id):
        yield
        DelayedFlagsHandler.DELAYED_ENABLED = False


def build_contract_kwargs(inputs):
    contract_kwargs = {}
    for key, input_type in inputs.items():
        if not issubclass(input_type, DelayedCollectionBase):
            contract_kwargs[key] = '{}|{}'.format(input_type.__name__, get_delayed_value_type(input_type).__name__)
        elif issubclass(input_type, DelayedDictBase):
            contract_kwargs[key] = 'dict(str:{})|dict(str:{})'.format(
                input_type.value_type.__name__,
                get_delayed_value_type(input_type.value_type).__name__
            )
        elif issubclass(input_type, DelayedListBase):
            contract_kwargs[key] = 'list({real})|list({delayed})'.format(
                real=input_type.value_type.__name__,
                delayed=get_delayed_value_type(input_type.value_type).__name__
            )
        else:
            raise TypeError("Unknown DelayedCollection derived type: {}".format(input_type.__name__))
    return contract_kwargs


def delayed_function(outputs, inputs):
    check_all_are_types('outputs', outputs)
    check_all_are_types('inputs', list(inputs.values()))

    contract_kwargs = build_contract_kwargs(inputs)

    def inner_decorator(func):
        validate_function(func)

        @functools.wraps(func)
        def delayed_function_wrapper(*args, **kwargs):
            do_type_check(func, args, kwargs, contract_kwargs)
            if DelayedFlagsHandler.DELAYED_ENABLED:
                func_args = inspect.getcallargs(func, *args, **kwargs)

                delayed_inputs = generate_delayed_inputs(func_args, inputs)
                delayed_func = generate_delayed_function_call(delayed_function_wrapper)
                delayed_outputs = generate_delayed_outputs(outputs)

                register_function_call(delayed_inputs, delayed_func, delayed_outputs)

                return convert_to_python_return(delayed_outputs)
            else:
                return func(*args, **kwargs)

        delayed_function_wrapper.inputs = deepcopy(inputs)
        delayed_function_wrapper.outputs = deepcopy(outputs)
        delayed_function_wrapper.func = func
        return delayed_function_wrapper

    return inner_decorator
