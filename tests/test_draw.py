from utils.draw_digraph import draw_graph
import networkx as nx


def test_draw_graph():
    # This is just a "smoke" test that drawing does not fail with exceptions
    G = nx.DiGraph()
    G.add_nodes_from(list(range(5)))
    G.add_edge(0, 2)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(2, 4)
    draw_graph(G)
