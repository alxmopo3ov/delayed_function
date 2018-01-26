import networkx as nx
from utils.singleton import SingletonBase
import contextlib


class DependencyGraph(SingletonBase, nx.DiGraph):
    def __init__(self, dependency_graph_id):
        self.dependency_graph_id = dependency_graph_id
        self.lazy_values = set()
        self.lazy_callers = set()
        super(DependencyGraph, self).__init__(name="{}_{}".format(type(self).__name__, self.dependency_graph_id))

    def validate(self):
        for n in self.lazy_values:
            assert set(self.predecessors(n)).\
                union(set(self.successors(n))).\
                issubset(self.lazy_callers), "All neighbours of lazy_value nodes must be lazy_callers"
        for n in self.lazy_callers:
            assert set(self.predecessors(n)).\
                union(set(self.successors(n))).\
                issubset(self.lazy_values), "All neighbours of lazy_caller nodes must be lazy_values"

    def clear(self):
        self.lazy_callers = set()
        self.lazy_values = set()
        super(DependencyGraph, self).clear()


class DependencyGraphHandler(SingletonBase):
    __dependency_graph = None

    @property
    def dependency_graph(self):
        return self.__dependency_graph

    def __init__(self):
        self.set_current_dependency_graph("default")

    def set_current_dependency_graph(self, dependency_graph_id):
        self.__dependency_graph = DependencyGraph(dependency_graph_id)


H = DependencyGraphHandler()


@contextlib.contextmanager
def dependency_graph_context(dependency_graph_id):
    prev = H.dependency_graph.dependency_graph_id
    H.set_current_dependency_graph(dependency_graph_id)
    yield
    H.set_current_dependency_graph(prev)


def register_lazy_value_node(node):
    """
    We execute this method only in LazyValueBase's __init__, hence we will always execute it for each instance only once
    (unless you decide to break everything and execute it on your own)
    """
    H.dependency_graph.add_node(node)
    H.dependency_graph.lazy_values.add(node)


def register_lazy_caller_node(node):
    """
    We execute this method only in LazyCaller's __init__, hence we will always execute it for each instance only once
    (unless you decide to break everything and execute it on your own)
    """
    H.dependency_graph.add_node(node)
    H.dependency_graph.lazy_callers.add(node)
    return len(H.dependency_graph.lazy_callers) - 1


def register_function_call(inputs, func, outputs):
    """
    Register following delayed function evaluation:
    outputs = func(**inputs)
    """
    for input_name, input_value in inputs.items():
        H.dependency_graph.add_edge(input_value, func, {'input_name': input_name})

    for i, out in enumerate(outputs):
        H.dependency_graph.add_edge(func, out, {'output_id': i})
