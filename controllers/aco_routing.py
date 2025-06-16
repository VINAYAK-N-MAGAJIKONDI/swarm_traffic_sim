import random
import networkx as nx
import numpy as np
from sumolib import net

class ACORouting:
    def __init__(self, net_file='sumo_sim/map.net.xml', num_ants=10, num_iterations=50, alpha=1, beta=3, rho=0.5, q=1.0):
        self.graph = self.load_sumo_network(net_file)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha  # influence of pheromone
        self.beta = beta    # influence of heuristic (1/distance)
        self.rho = rho      # evaporation rate
        self.q = q          # pheromone deposit factor

        # Initialize pheromone on all edges
        self.pheromone = {edge: 1.0 for edge in self.graph.edges()}

    def load_sumo_network(self, net_file):
        sumo_net = net.readNet(net_file)
        G = nx.DiGraph()
        for edge in sumo_net.getEdges():
            from_node = edge.getFromNode().getID()
            to_node = edge.getToNode().getID()
            length = edge.getLength()
            G.add_edge(from_node, to_node, weight=length)
        return G

    def run(self, start_node, end_node):
        best_path = None
        best_cost = float('inf')

        for iteration in range(self.num_iterations):
            all_paths = []
            all_costs = []

            for _ in range(self.num_ants):
                path = self.construct_solution(start_node, end_node)
                if path:
                    cost = self.calculate_path_cost(path)
                    all_paths.append(path)
                    all_costs.append(cost)

                    if cost < best_cost:
                        best_cost = cost
                        best_path = path

            self.evaporate_pheromone()
            self.update_pheromone(all_paths, all_costs)

        return best_path

    def construct_solution(self, start, end):
        path = [start]
        visited = set()
        current = start

        while current != end:
            visited.add(current)
            neighbors = list(self.graph.successors(current))
            probabilities = []

            for neighbor in neighbors:
                if neighbor in visited:
                    probabilities.append(0)
                    continue

                edge = (current, neighbor)
                pheromone_level = self.pheromone[edge] ** self.alpha
                heuristic = (1.0 / self.graph[current][neighbor].get("weight", 1.0)) ** self.beta
                probabilities.append(pheromone_level * heuristic)

            if sum(probabilities) == 0:
                return None  # Dead end

            probabilities = [p / sum(probabilities) for p in probabilities]
            next_node = random.choices(neighbors, weights=probabilities)[0]
            path.append(next_node)
            current = next_node

        return path

    def calculate_path_cost(self, path):
        return sum(self.graph[path[i]][path[i + 1]].get("weight", 1.0) for i in range(len(path) - 1))

    def evaporate_pheromone(self):
        for edge in self.pheromone:
            self.pheromone[edge] *= (1 - self.rho)

    def update_pheromone(self, paths, costs):
        for path, cost in zip(paths, costs):
            for i in range(len(path) - 1):
                edge = (path[i], path[i + 1])
                self.pheromone[edge] += self.q / cost

def calculate_optimal_route(start, end, net_file='sumo_sim/map.net.xml'):
    aco = ACORouting(net_file=net_file)
    return aco.run(start, end)

