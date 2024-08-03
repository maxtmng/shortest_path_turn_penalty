from heapq import heappop, heappush
from itertools import count
import networkx as nx


def shortest_path_turn_penalty(G, source, target, weight="travel_time", penalty={}, next_node=None):
    """
    Uses Dijkstra's algorithm to find the shortest weighted paths to one or multiple targets with turn penalty.
    This function is adapted from networkx.algorithms.shortest_paths.weighted._dijkstra_multisource.
    The turn penalty implementation is based on:
    Ziliaskopoulos, A.K., Mahmassani, H.S., 1996. A note on least time path computation considering delays and prohibitions for intersection movements. Transportation Research Part B: Methodological 30, 359–367. https://doi.org/10.1016/0191-2615(96)00001-X


    Parameters
    ----------
    G : NetworkX graph

    source : non-empty iterable of nodes
        Starting nodes for paths. If this is just an iterable containing
        a single node, then all paths computed by this function will
        start from that node. If there are two or more nodes in this
        iterable, the computed paths may begin from any one of the start
        nodes.

    target : node label, single node or a list
        Ending node (or a list of ending nodes) for path. Search is halted when any target is found.

    weight: function
        Function with (u, v, data) input that returns that edge's weight
        or None to indicate a hidden edge

    penalty : dict, optional (default={})
        Dictionary containing turn penalties. The key is a tuple (u, v, m) where
        u, v are the nodes of the current edge and m is the next node.

    next_node : node, optional (default=None)
        Next node to consider from the source.

    Returns
    -------
    list of nodes
        Path from source to target.

    Raises
    ------
    NodeNotFound
        If the source or target is not in `G`.

    ValueError
        If contradictory paths are found due to negative weights.
    """

    G_succ = G._adj  # For speed-up (and works for both directed and undirected graphs)
    weight = nx.algorithms.shortest_paths.weighted._weight_function(G, weight)
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    paths = {source: [source]}
    target_list = [target] if not isinstance(target, list) else target
    reached_target = None

    seen = {source: {}}
    c = count()
    fringe = []

    if next_node is None:
        for m, _ in G_succ[source].items():
            seen[source][m] = 0
            push(fringe, (0, next(c), source, m))
    else:
        push(fringe, (0, next(c), source, next_node))

    while fringe:
        (d, _, v, m) = pop(fringe)
        u = m
        if v in dist:
            if u in dist[v]:
                continue  # already searched this node.
        else:
            dist[v] = {}
        dist[v][u] = d

        if v in target_list:
            reached_target = v
            break

        e = G[v][u]
        for m in G_succ[u]:
            cost = weight(v, u, e)
            if (v, u, m) in penalty:
                cost += penalty[v, u, m]

            if cost is None:
                continue
            vu_dist = dist[v][u] + cost
            if u in dist:
                if m in dist[u]:
                    u_dist = dist[u][m]
                    if vu_dist < u_dist:
                        raise ValueError("Contradictory paths found:", "negative weights?")
            elif u not in seen or m not in seen[u] or vu_dist < seen[u][m]:
                if u not in seen:
                    seen[u] = {}
                seen[u][m] = vu_dist
                push(fringe, (vu_dist, next(c), u, m))
                if paths is not None:
                    paths[u] = paths[v] + [u]

    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
    return paths[reached_target]
