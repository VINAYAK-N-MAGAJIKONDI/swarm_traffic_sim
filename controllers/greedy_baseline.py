# Greedy routing and signal control baselines
import networkx as nx

def greedy_route(graph: nx.DiGraph, start, end):
    # Always pick the neighbor with the shortest edge to the destination
    path = [start]
    current = start
    while current != end:
        neighbors = list(graph.successors(current))
        if not neighbors:
            break
        # Pick neighbor with minimum edge weight
        next_node = min(neighbors, key=lambda n: graph[current][n].get('weight', 1.0))
        path.append(next_node)
        current = next_node
    return path

def greedy_signal_timing(traffic_data):
    # Always give green to the approach with the most vehicles
    # Placeholder: return index of max traffic
    return max(range(len(traffic_data)), key=lambda i: traffic_data[i])
