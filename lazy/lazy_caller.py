from graph.dependency_graph import register_lazy_caller_node


class LazyCaller(object):
    def __init__(self, func):
        self.func = func
        self.__caller_id = register_lazy_caller_node(self)

    @property
    def caller_id(self):
        return self.__caller_id

    def __repr__(self):
        return "{}[{}]".format(type(self).__name__, self.func.__name__)


def generate_lazy_function_call(func):
    return LazyCaller(func)
