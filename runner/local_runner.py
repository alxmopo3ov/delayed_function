from graph.computation_graph import convert_dependency_graph_to_computation_graph
from serialize.initialized_value_storage import initialized_value_storage
from serialize.serialization_handler import SerializationHandler
from executable_container.local_container import LocalContainer
from graph.dependency_graph import H, dependency_graph_context
from delayed.delayed_value import DelayedListBase, DelayedDictBase
import networkx as nx


def build_inputs(node):
    res = {}
    input_types = node.func.inputs
    # collect all inputs for names dictionaries
    for inp in H.dependency_graph.predecessors(node):
        input_name = H.dependency_graph.get_edge_data(inp, node)['input_name']
        if issubclass(input_types[input_name], (DelayedListBase, DelayedDictBase)):
            input_key = H.dependency_graph.get_edge_data(inp, node)['input_key']
            res.setdefault(input_name, {})[input_key] = inp
        else:
            res[input_name] = inp

    return res


def run_local(dependency_graph_id):
    """
    Simple single-threaded local runner.
    """
    with dependency_graph_context(dependency_graph_id):
        computation_graph = convert_dependency_graph_to_computation_graph()
        h = SerializationHandler()
        evaluated_serialized = {key: h.serialize(value) for key, value in initialized_value_storage.items()}

        # Networkx reversed graph works very weirdly. When doing it by myself, it works fine (no crutch!)
        reversed_graph = nx.DiGraph()
        reversed_graph.add_nodes_from(computation_graph.nodes())
        reversed_graph.add_edges_from((y, x) for x, y in computation_graph.edges())

        # iterate over delayed callers
        for node in nx.dfs_postorder_nodes(reversed_graph):
            inputs_dict = build_inputs(node)
            outputs_dict = {H.dependency_graph.get_edge_data(node, out)['output_id']: out
                            for out in H.dependency_graph.successors(node)}
            container = LocalContainer(inputs_dict, node.func, outputs_dict, evaluated_serialized)
            container.run()

    return {key: h.deserialize(value, key.value_type) for key, value in evaluated_serialized.items()}
