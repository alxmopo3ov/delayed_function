import functools
import inspect

from lazy.lazy_value import get_lazy_value_type, LazyValueBase

from graph.dependency_graph import register_function_call
from lazy.lazy_caller import generate_lazy_function_call
from utils.type_check import do_type_check


def check_all_are_types(out, args):
    if not all(isinstance(x, type) for x in args):
        raise TypeError("All {} arguments must be types, not objects. Got: {}".format(out, args))


def generate_lazy_outputs(output_types):
    if output_types:
        return tuple(get_lazy_value_type(x)() for x in output_types)
    else:
        return ()


def convert_to_lazy_value(value):
    """
    When pickled, the value will be stored in closure of the inner function and hence uploaded with the pickled func
    :param value: some value to store
    :return: function that returns this value
    """
    @lazy_function(type(value))
    def value_keeper():
        return value

    return value_keeper()


def generate_lazy_inputs(values):
    return {key: value if isinstance(value, LazyValueBase) else convert_to_lazy_value(value) for key, value in values.items()}


def validate_function(func):
    argspec = inspect.getfullargspec(func)
    if argspec.varargs or argspec.varkw:
        raise TypeError("Using varargs or varkwargs (for example, def myfunc(*args, **kwargs)) "
                        "is forbidden for lazy functions")


def convert_to_python_return(outputs_tuple):
    if len(outputs_tuple) == 0:
        return None
    elif len(outputs_tuple) == 1:
        return outputs_tuple[0]
    else:
        return outputs_tuple


def lazy_function(*outputs, **inputs):
    check_all_are_types('outputs', outputs)
    check_all_are_types('inputs', list(inputs.values()))

    contract_kwargs = {key: '{}|{}'.format(input_type.__name__, get_lazy_value_type(input_type).__name__)
                       for key, input_type in inputs.items()}

    def inner_decorator(func):
        validate_function(func)

        @functools.wraps(func)
        def lazy_function_wrapper(*args, **kwargs):
            do_type_check(func, args, kwargs, contract_kwargs)
            # this line will obtain not only values from args and kwargs that we provided explicitly,
            # but also default arguments of func we did not mention
            func_args = inspect.getcallargs(func, *args, **kwargs)

            lazy_inputs = generate_lazy_inputs(func_args)
            lazy_func = generate_lazy_function_call(func)
            lazy_outputs = generate_lazy_outputs(outputs)

            register_function_call(lazy_inputs, lazy_func, lazy_outputs)

            return convert_to_python_return(lazy_outputs)
        return lazy_function_wrapper

    return inner_decorator
