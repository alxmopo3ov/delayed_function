from graph.dependency_graph import register_delayed_caller_node


class DelayedCaller(object):
    def __init__(self, func):
        self.func = func
        self.__caller_id = register_delayed_caller_node(self)

    @property
    def caller_id(self):
        return self.__caller_id

    def __repr__(self):
        return "{}[{}]".format(type(self).__name__, self.func.__name__)


def generate_delayed_function_call(func):
    return DelayedCaller(func)
