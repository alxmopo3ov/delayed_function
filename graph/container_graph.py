import networkx as nx
from graph.dependency_graph import H


class ContainerGraphOutputNode(object):
    def __init__(self, value_type, output_id):
        self.value_type = value_type
        self.output_id = output_id

    def __repr__(self):
        return "{} out_{}".format(self.value_type.__name__, self.output_id)


class ContainerGraphInputNode(object):
    def __init__(self, value_type, name):
        self.value_type = value_type
        self.name = name

    def __repr__(self):
        return self.value_type.__name__ + " " + self.name


def convert_dependency_graph_to_container_graph():
    """
    Container graph is used in cloud environment such as Nirvana or Nirvana/Reactor to define isolated
    containers with functions, function inputs and outputs, connect them and delegate all computation
    to cloud system
    :return: 
    """
    dependency_graph = H.dependency_graph
    dependency_graph.validate()
    G = nx.DiGraph()
    for n in dependency_graph.lazy_values:
        predecessor = dependency_graph.predecessors(n)[0]
        successors = dependency_graph.successors(n)
        G.add_nodes_from([predecessor] + successors)

        out = ContainerGraphOutputNode(
            value_type=n.value_type,
            output_id=dependency_graph.get_edge_data(predecessor, n)['output_id']
        )
        G.add_node(out)
        G.add_edge(predecessor, out)

        cur_inputs = [
            ContainerGraphInputNode(
                name=dependency_graph.get_edge_data(n, s)['input_name'],
                value_type=n.value_type
            )
            for s in successors
        ]
        G.add_nodes_from(cur_inputs)
        for inp, succ in zip(cur_inputs, successors):
            G.add_path([out, inp, succ])
    return G
