from utils.marked_graph import create_marked_graph
import networkx as nx
import matplotlib.pyplot as plt
import warnings


def draw_graph(basic_graph, figsize=(16, 8), normalize=True):
    G, pos = create_marked_graph(basic_graph, normalize=normalize)
    f, axs = plt.subplots(1, 1, figsize=figsize)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        nx.draw(G, pos=pos, with_labels=True, ax=axs)
