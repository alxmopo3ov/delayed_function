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


# seems to be tested too!
def mark_dfs(G, source, normalize=True):
    marks_dict = {}
    marks_dict = {i: 0 for i in range(max([n.bfs_mark for n in G]) + 1)}

    visited = set()

    def _mark_dfs(G, source, rank=0):
        local_rank = marks_dict[rank]
        source.set_dfs_mark(local_rank)
        marks_dict[rank] += 1
        visited.add(source)
        for n in G.successors(source):
            if n not in visited:
                _mark_dfs(G, n, rank + 1)

    _mark_dfs(G, source)

    if normalize:
        total_max_rank = max(n.dfs_mark for n in G)
        visited = set()

        def _normalize_dfs(G, source, rank=0):
            local_max_rank = marks_dict[rank]
            new_mark = total_max_rank / (local_max_rank + 1) * (source.dfs_mark + 1)
            source.dfs_mark = new_mark
            visited.add(source)
            for n in G.successors(source):
                if n not in visited:
                    _normalize_dfs(G, n, rank + 1)

        _normalize_dfs(G, source)


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
    mark_dfs(G, fake_root, normalize=normalize)

    pos = {n: (n.dfs_mark, n.bfs_mark) for n in G}
    pos.pop(fake_root)
    G.remove_node(fake_root)

    return G, pos
