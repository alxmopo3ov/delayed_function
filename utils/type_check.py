import contracts
import inspect
import copy


def build_func_with_same_signature(func):
    argspec = inspect.getargspec(func)
    defaults = tuple() if argspec.defaults is None else argspec.defaults
    if len(defaults):
        arg_string = ", ".join(
            argspec.args[:-len(defaults)] +
            ["{}={}".format(x, repr(y)) for x, y in zip(argspec.args[-len(defaults):], defaults)]
        )
    else:
        arg_string = ", ".join(argspec.args)
    exec("""
def dummy_func({args}):\n
    pass\n
""".format(args=arg_string), locals(), locals())
    return locals()['dummy_func']


def do_type_check(func, args, kwargs, contract_kwargs):
    if not contract_kwargs:
        # function has no arguments; nothing to do here
        return
    type_check_func = copy.deepcopy(build_func_with_same_signature(func))
    type_check_func.__name__ = func.__name__
    type_check_func = contracts.contract(**contract_kwargs)(type_check_func)
    type_check_func(*args, **kwargs)
