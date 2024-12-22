import math


def is_left_turn(bearing1, bearing2):
    relative_bearing = (bearing2 - bearing1) % 360
    return 150 < relative_bearing < 330


def is_right_turn(bearing1, bearing2):
    relative_bearing = (bearing2 - bearing1) % 360
    return 30 < relative_bearing <= 150


def calculate_bearing(G, u, v):
    lat1, lon1 = G.nodes[u]['y'], G.nodes[u]['x']
    lat2, lon2 = G.nodes[v]['y'], G.nodes[v]['x']
    delta_lon = lon2 - lon1
    y = math.sin(math.radians(delta_lon)) * math.cos(math.radians(lat2))
    x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(
        math.radians(lat2)) * math.cos(math.radians(delta_lon))
    initial_bearing = math.atan2(y, x)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing


def penalty_turns(G, left_turn_penalty=60, right_turn_penalty=30):
    """
    Calculate turn penalties for each node pair
    :param G: NetworkX graph (directed or undirected)
    :param left_turn_penalty: in s
    :param right_turn_penalty: in s
    :return: penalty dictionary
    """
    penalty = {}

    for node in G.nodes():
        # Handle both directed and undirected graphs
        if hasattr(G, 'in_edges'):  # DiGraph
            in_edges = list(G.in_edges(node, data=True))
            out_edges = list(G.out_edges(node, data=True))
        else:  # Undirected Graph
            edges = list(G.edges(node, data=True))
            # For undirected graphs, all edges can be both incoming and outgoing
            in_edges = [(u, v, d) for u, v, d in edges if v == node]
            out_edges = [(u, v, d) for u, v, d in edges if u == node]

        for u, _, data_in in in_edges:
            for _, v, data_out in out_edges:
                if is_left_turn(data_in['bearing'], data_out['bearing']):
                    penalty[u, node, v] = left_turn_penalty
                elif is_right_turn(data_in['bearing'], data_out['bearing']):
                    penalty[u, node, v] = right_turn_penalty

    return penalty
