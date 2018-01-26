import inspect


def validate_function(func):
    argspec = inspect.getfullargspec(func)
    if argspec.varargs or argspec.varkw:
        raise TypeError("Using varargs or varkwargs (for example, def myfunc(*args, **kwargs)) "
                        "is forbidden for delayed functions")


def convert_to_python_return(outputs_tuple):
    if len(outputs_tuple) == 0:
        return None
    elif len(outputs_tuple) == 1:
        return outputs_tuple[0]
    else:
        return outputs_tuple


def check_all_are_types(out, args):
    if not all(isinstance(x, type) for x in args):
        raise TypeError("All {} arguments must be types, not objects. Got: {}".format(out, args))
