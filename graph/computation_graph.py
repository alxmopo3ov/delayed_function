from graph.dependency_graph import H
import networkx as nx
import itertools


def convert_dependency_graph_to_computation_graph():
    """
    Computation graph is used in local backend to make function traversal more easy
    :return: 
    """
    H.dependency_graph.validate()
    G = nx.DiGraph()
    for n in H.dependency_graph.lazy_values:
        for p, s in itertools.product(H.dependency_graph.predecessors(n), H.dependency_graph.successors(n)):
            G.add_nodes_from([p, s])
            G.add_edge(p, s)
    return G
