from collections import deque
import networkx as nx


class FakeNode(object):
    def __init__(self, name):
        self.name = name
        self.bfs_mark = -1
        self.dfs_mark = -1

    def set_bfs_mark(self, mark):
        self.bfs_mark = max(mark, self.bfs_mark)

    def set_dfs_mark(self, mark):
        self.dfs_mark = max(mark, self.dfs_mark)

    def __repr__(self):
        return self.name


# seems to be tested!
def mark_bfs(G, source):
    source.set_bfs_mark(0)
    neighbors = G.neighbors_iter
    queue = deque([(source, neighbors(source))])
    while queue:
        parent, children = queue[0]
        try:
            child = next(children)
            child.set_bfs_mark(parent.bfs_mark + 1)
            queue.append((child, neighbors(child)))
        except StopIteration:
            queue.popleft()

    # reverse all marks
    max_mark = max(n.bfs_mark for n in G)
    for n in G:
        n.bfs_mark = max_mark - n.bfs_mark


def mark_dfs(G, normalize=True):
    marks_dict = {}
    for n in nx.dfs_postorder_nodes(G):
        n.set_dfs_mark(marks_dict.setdefault(n.bfs_mark, 0))
        marks_dict[n.bfs_mark] += 1

    if normalize:
        for node in G:
            node.dfs_mark = 1.0 / (marks_dict[node.bfs_mark] + 1.0) * (node.dfs_mark + 1.0)


def create_marked_graph(basic_graph, normalize=True):
    G = nx.DiGraph()

    ids_dict = {id(x): FakeNode(repr(x)) for x in basic_graph}
    G.add_nodes_from(ids_dict.values())
    for u, v in basic_graph.edges():
        G.add_edge(ids_dict[id(u)], ids_dict[id(v)])

    # adds fake root
    fake_root = FakeNode("fake_root")
    nodes_without_predecessors = [x for x in G.nodes() if not G.predecessors(x)]
    G.add_node(fake_root)
    G.add_edges_from([(fake_root, p) for p in nodes_without_predecessors])

    mark_bfs(G, fake_root)
    mark_dfs(G, normalize=normalize)

    pos = {n: (n.dfs_mark, n.bfs_mark) for n in G}
    pos.pop(fake_root)
    G.remove_node(fake_root)

    return G, pos
