import functools
import inspect
import contextlib
from copy import deepcopy
from delayed.delayed_value import get_delayed_value_type, DelayedValueBase, convert_to_delayed_value
from delayed.delayed_caller import generate_delayed_function_call
from delayed.delayed_utils import check_all_are_types, validate_function, convert_to_python_return
from graph.dependency_graph import register_function_call, dependency_graph_context
from utils.type_check import do_type_check


class DelayedFlagsHandler(object):
    DELAYED_ENABLED = False


@contextlib.contextmanager
def build_dependency_graph(dependency_graph_id):
    DelayedFlagsHandler.DELAYED_ENABLED = True
    with dependency_graph_context(dependency_graph_id):
        yield
        DelayedFlagsHandler.DELAYED_ENABLED = False


def generate_delayed_outputs(output_types):
    if output_types:
        return tuple(get_delayed_value_type(x)() for x in output_types)
    else:
        return ()


def generate_delayed_inputs(values):
    return {key: value if isinstance(value, DelayedValueBase) else convert_to_delayed_value(value) for key, value in values.items()}


def delayed_function(outputs, inputs, container_params=None, environment_params=None):
    check_all_are_types('outputs', outputs)
    check_all_are_types('inputs', list(inputs.values()))

    contract_kwargs = {key: '{}|{}'.format(input_type.__name__, get_delayed_value_type(input_type).__name__)
                       for key, input_type in inputs.items()}

    def inner_decorator(func):
        validate_function(func)

        @functools.wraps(func)
        def delayed_function_wrapper(*args, **kwargs):
            do_type_check(func, args, kwargs, contract_kwargs)
            if DelayedFlagsHandler.DELAYED_ENABLED:
                func_args = inspect.getcallargs(func, *args, **kwargs)

                delayed_inputs = generate_delayed_inputs(func_args)
                delayed_func = generate_delayed_function_call(delayed_function_wrapper)
                delayed_outputs = generate_delayed_outputs(outputs)

                register_function_call(delayed_inputs, delayed_func, delayed_outputs)

                return convert_to_python_return(delayed_outputs)
            else:
                return func(*args, **kwargs)

        delayed_function_wrapper.container_params = deepcopy(container_params)
        delayed_function_wrapper.environment_params = deepcopy(environment_params)
        delayed_function_wrapper.inputs = deepcopy(inputs)
        delayed_function_wrapper.outputs = deepcopy(outputs)
        delayed_function_wrapper.func = func
        return delayed_function_wrapper

    return inner_decorator
