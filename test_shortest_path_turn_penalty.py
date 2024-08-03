import pytest
import osmnx as ox
import os
from shortest_path_util import penalty_turns
from shortest_path_turn_penalty import shortest_path_turn_penalty


@pytest.fixture
def graph():
    # Define the bounding box coordinates
    north, south, east, west = 41.89, 41.87, -87.64, -87.62
    test_network = 'test_network.graphml'

    if os.path.exists(test_network):
        G = ox.load_graphml(test_network)
    else:
        # Download the street network within this bounding box
        G = ox.graph_from_bbox(north, south, east, west, network_type='drive')

        # Save the network to disk
        ox.save_graphml(G, filepath=test_network)

    # Add edge bearings
    G = ox.add_edge_bearings(G)

    # Remove self-loop edges
    self_loop_edges = []
    for u, v, data in G.edges(data=True):
        if u == v:
            self_loop_edges.append((u, v))
    G.remove_edges_from(self_loop_edges)

    return G


def test_shortest_path_turn_penalty(graph):
    penalty = penalty_turns(graph)

    result = shortest_path_turn_penalty(graph, 271169073, 740243448, weight="travel_time", penalty=penalty)

    expected_output = [271169073, 271169072, 270611554, 258957316, 258957340, 10923165760,
                       28290296, 11060811046, 28289318, 740243448]

    assert result == expected_output, f"Expected {expected_output}, but got {result}"


if __name__ == "__main__":
    pytest.main([__file__])