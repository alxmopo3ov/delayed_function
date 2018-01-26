from graph.computation_graph import convert_dependency_graph_to_computation_graph
from serialize.initialized_value_storage import initialized_value_storage
from executable_container.local_container import LocalContainer
from graph.dependency_graph import H, dependency_graph_context
import networkx as nx
from copy import deepcopy


def run_local(dependency_graph_id):
    """
    Simple single-threaded local runner.
    """
    with dependency_graph_context(dependency_graph_id):
        computation_graph = convert_dependency_graph_to_computation_graph()
        lazy_values_evaluated = deepcopy(initialized_value_storage)

        # Networkx reversed graph works very weirdly. When doing it by myself, it works fine (no crutch!)
        reversed_graph = nx.DiGraph()
        reversed_graph.add_nodes_from(computation_graph.nodes())
        reversed_graph.add_edges_from((y, x) for x, y in computation_graph.edges())

        # iterate over lazy callers
        for node in nx.dfs_postorder_nodes(reversed_graph):
            inputs_dict = {H.dependency_graph.get_edge_data(inp, node)['input_name']: inp
                           for inp in H.dependency_graph.predecessors(node)}
            outputs_dict = {H.dependency_graph.get_edge_data(node, out)['output_id']: out
                            for out in H.dependency_graph.successors(node)}
            container = LocalContainer(inputs_dict, node.func, outputs_dict, lazy_values_evaluated)
            container.run()

    return lazy_values_evaluated