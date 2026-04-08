import math


def is_left_turn(bearing1, bearing2):
    relative_bearing = (bearing2 - bearing1) % 360
    return 150 < relative_bearing < 330


def is_right_turn(bearing1, bearing2):
    relative_bearing = (bearing2 - bearing1) % 360
    return 30 < relative_bearing <= 150


def calculate_bearing(G, u, v, projected=False):
    """
    Calculate compass bearing between two nodes in a graph.

    :param G: NetworkX graph with 'x' and 'y' node attributes
    :param u: source node
    :param v: target node
    :param projected: if True, assumes coordinates are in a projected CRS (e.g. UTM)
                      where distances can be measured directly.
                      If False (default), assumes geographic coordinates (lat/lon in degrees).
    :return: compass bearing in degrees (0-360, 0=north, 90=east)
    """
    y1, x1 = G.nodes[u]['y'], G.nodes[u]['x']
    y2, x2 = G.nodes[v]['y'], G.nodes[v]['x']

    if projected:
        delta_x = x2 - x1
        delta_y = y2 - y1
        initial_bearing = -(math.atan2(delta_y, delta_x) - math.pi / 2)
    else:
        delta_lon = x2 - x1
        y = math.sin(math.radians(delta_lon)) * math.cos(math.radians(y2))
        x = math.cos(math.radians(y1)) * math.sin(math.radians(y2)) - math.sin(math.radians(y1)) * math.cos(
            math.radians(y2)) * math.cos(math.radians(delta_lon))
        initial_bearing = math.atan2(y, x)

    compass_bearing = (math.degrees(initial_bearing) + 360) % 360
    return compass_bearing


def penalty_turns(G, left_turn_penalty=60, right_turn_penalty=30, projected=False):
    """
    Calculate turn penalties for each node pair
    :param G: NetworkX graph (directed or undirected)
    :param left_turn_penalty: in s
    :param right_turn_penalty: in s
    :param projected: if True, assumes node coordinates are in a projected CRS (e.g. UTM).
                      Only used for undirected graphs where bearings are computed dynamically.
    :return: penalty dictionary
    """
    penalty = {}

    for node in G.nodes():
        # Handle both directed and undirected graphs
        if hasattr(G, 'in_edges'):  # DiGraph
            in_edges = list(G.in_edges(node, data=True))
            out_edges = list(G.out_edges(node, data=True))
        else:  # Undirected Graph
            in_edges = []
            out_edges = []

            for _, neighbor, data in G.edges(node, data=True):
                bearing_in = calculate_bearing(G, neighbor, node, projected=projected)
                bearing_out = calculate_bearing(G, node, neighbor, projected=projected)

                in_edges.append((neighbor, node, {'bearing': bearing_in}))
                out_edges.append((node, neighbor, {'bearing': bearing_out}))

        for u, _, data_in in in_edges:
            for _, v, data_out in out_edges:
                if u == v:
                    continue
                if is_left_turn(data_in['bearing'], data_out['bearing']):
                    penalty[u, node, v] = left_turn_penalty
                elif is_right_turn(data_in['bearing'], data_out['bearing']):
                    penalty[u, node, v] = right_turn_penalty

    return penalty
