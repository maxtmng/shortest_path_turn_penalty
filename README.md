# shortest_path_turn_penalty

This project implements a modified Dijkstra's algorithm to find the shortest weighted paths in a graph while considering turn penalties at intersections. It's particularly useful for routing applications in road networks where turn delays significantly impact travel times.

## Features

- Calculates shortest paths with consideration for turn penalties
- Supports both directed and undirected graphs
- Supports both left and right turn penalties
- Supports geographic (lat/lon) and projected (e.g. UTM) coordinate systems
- Uses OpenStreetMap data for real-world road networks
- Includes utility functions for calculating bearings and identifying turn types

## Algorithm Details

The main function is adapted from `networkx.algorithms.shortest_paths.weighted._dijkstra_multisource`. It uses Dijkstra's algorithm to find the shortest weighted paths to one or multiple targets with turn penalty.

The turn penalty implementation is based on the work of Ziliaskopoulos and Mahmassani (1996):

Ziliaskopoulos, A.K., Mahmassani, H.S., 1996. A note on least time path computation considering delays and prohibitions for intersection movements. Transportation Research Part B: Methodological 30, 359–367. https://doi.org/10.1016/0191-2615(96)00001-X

## Installation

To use this project, you'll need to install the following dependencies:

```bash
pip install networkx osmnx pytest
```

## Usage

The main function `shortest_path_turn_penalty` is located in `shortest_path_turn_penalty.py`. Here's a basic example of how to use it:

```python
from shortest_path_util import penalty_turns
from shortest_path_turn_penalty import shortest_path_turn_penalty

# Load or create your graph (directed or undirected)
# G = ...

# Calculate turn penalties
penalty = penalty_turns(G)

# Find the shortest path
path = shortest_path_turn_penalty(G, source_node, target_node, weight="travel_time", penalty=penalty)
```

### Projected coordinates (e.g. UTM)

By default, `calculate_bearing` and `penalty_turns` assume geographic coordinates (lat/lon in degrees). If your graph uses a projected CRS such as UTM, pass `projected=True`:

```python
penalty = penalty_turns(G, projected=True)
```

### Directed vs. undirected graphs

Both directed and undirected graphs are supported. For directed graphs, `penalty_turns` uses the pre-computed `bearing` edge attribute (e.g. from `osmnx.add_edge_bearings`). For undirected graphs, bearings are computed dynamically from node coordinates.

## Testing

The project includes a test suite in `test_shortest_path_turn_penalty.py`. To run the tests:

```bash
pytest test_shortest_path_turn_penalty.py
```

The test suite uses a sample road network from OpenStreetMap, which is downloaded and cached locally for subsequent runs.

## Files

- `shortest_path_turn_penalty.py`: Contains the main algorithm implementation.
- `shortest_path_util.py`: Includes utility functions for turn penalty calculations and bearing computations.
- `test_shortest_path_turn_penalty.py`: Contains the test suite for the algorithm.

## Contributing

Contributions to improve the algorithm or extend its functionality are welcome. Please feel free to submit issues or pull requests.
