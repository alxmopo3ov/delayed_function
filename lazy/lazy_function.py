import functools
import inspect
import contextlib
from copy import deepcopy
from lazy.lazy_value import get_lazy_value_type, LazyValueBase, convert_to_lazy_value
from lazy.lazy_caller import generate_lazy_function_call
from lazy.lazy_utils import check_all_are_types, validate_function, convert_to_python_return
from graph.dependency_graph import register_function_call, dependency_graph_context
from utils.type_check import do_type_check


LAZY_ENABLED = False


@contextlib.contextmanager
def build_dependency_graph(dependency_graph_id):
    global LAZY_ENABLED
    LAZY_ENABLED = True
    with dependency_graph_context(dependency_graph_id):
        yield
    LAZY_ENABLED = False


def generate_lazy_outputs(output_types):
    if output_types:
        return tuple(get_lazy_value_type(x)() for x in output_types)
    else:
        return ()


def generate_lazy_inputs(values):
    return {key: value if isinstance(value, LazyValueBase) else convert_to_lazy_value(value) for key, value in values.items()}


def lazy_function(outputs, inputs, container_params=None, environment_params=None):
    check_all_are_types('outputs', outputs)
    check_all_are_types('inputs', list(inputs.values()))

    contract_kwargs = {key: '{}|{}'.format(input_type.__name__, get_lazy_value_type(input_type).__name__)
                       for key, input_type in inputs.items()}

    def inner_decorator(func):
        validate_function(func)

        @functools.wraps(func)
        def lazy_function_wrapper(*args, **kwargs):
            do_type_check(func, args, kwargs, contract_kwargs)
            if LAZY_ENABLED:
                func_args = inspect.getcallargs(func, *args, **kwargs)

                lazy_inputs = generate_lazy_inputs(func_args)
                lazy_func = generate_lazy_function_call(lazy_function_wrapper)
                lazy_outputs = generate_lazy_outputs(outputs)

                register_function_call(lazy_inputs, lazy_func, lazy_outputs)

                return convert_to_python_return(lazy_outputs)
            else:
                return func(*args, **kwargs)

        lazy_function_wrapper.container_params = deepcopy(container_params)
        lazy_function_wrapper.environment_params = deepcopy(environment_params)
        lazy_function_wrapper.inputs = deepcopy(inputs)
        lazy_function_wrapper.outputs = deepcopy(outputs)
        lazy_function_wrapper.func = func
        return lazy_function_wrapper

    return inner_decorator
