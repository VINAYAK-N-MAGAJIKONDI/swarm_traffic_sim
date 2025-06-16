# Random routing and signal control baselines
import networkx as nx
import random

def random_route(graph: nx.DiGraph, start, end):
    # Randomly select next node until destination is reached
    path = [start]
    current = start
    while current != end:
        neighbors = list(graph.successors(current))
        if not neighbors:
            break
        next_node = random.choice(neighbors)
        path.append(next_node)
        current = next_node
    return path

def random_signal_timing(traffic_data):
    # Randomly select a signal phase
    return random.randint(0, len(traffic_data)-1)
