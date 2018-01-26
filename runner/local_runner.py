from graph.computation_graph import convert_dependency_graph_to_computation_graph
from graph.container_graph import convert_dependency_graph_to_container_graph
from executable_container.container_factory import build_container
import networkx as nx


def run_local():
    """
    Simple single-threaded local runner.
    """
    container_graph = convert_dependency_graph_to_container_graph()
    computation_graph = convert_dependency_graph_to_computation_graph()

    # Networkx reversed graph works very weirdly. When doing it by myself, it works fine (no crutch!)
    reversed_graph = nx.DiGraph()
    reversed_graph.add_nodes_from(computation_graph.nodes())
    reversed_graph.add_edges_from((y, x) for x, y in computation_graph.edges())

    for node in nx.dfs_postorder_nodes(reversed_graph):
        container = build_container('local', node.func)
        container.run()
