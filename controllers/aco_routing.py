import random
import networkx as nx
import numpy as np
from sumolib import net

class ACORouting:
    def __init__(self,
                 net_file='sumo_sim/grid.net.xml',
                 num_ants=40,
                 num_iterations=100,
                 alpha_min=1.0,
                 alpha_max=2.5,
                 beta=5.0,
                 rho=0.2,
                 Q=50,
                 lambda_congestion=2.0,
                 lambda_signal=1.5,
                 tau_min=0.01,
                 tau_max=10):

        self.graph = self.load_sumo_network(net_file)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.lambda_congestion = lambda_congestion
        self.lambda_signal = lambda_signal
        self.tau_min = tau_min
        self.tau_max = tau_max

        self.pheromone = {edge: 1.0 for edge in self.graph.edges()}
        self.best_global_cost = float("inf")
        self.best_global_path = None

    def load_sumo_network(self, net_file):
        sumo_net = net.readNet(net_file)
        G = nx.DiGraph()

        for edge in sumo_net.getEdges():
            G.add_edge(
                edge.getFromNode().getID(),
                edge.getToNode().getID(),
                id=edge.getID(),
                length=edge.getLength(),
                speed=edge.getSpeed(),
                capacity=max(edge.getLaneNumber() * 1800, 1)
            )
        return G

    def update_weights(self, traffic_data):
        """Calculates dynamic costs based on IEEE standard: time, normalized queue, and signals."""
        for u, v, data in self.graph.edges(data=True):
            edge_id = data["id"]
            length = data["length"]
            speed_limit = data["speed"]
            capacity = data["capacity"]

            state = traffic_data.get(edge_id, {})
            mean_speed = max(state.get("mean_speed", speed_limit), 0.1)
            queue = state.get("halting_number", 0)
            signal_delay = state.get("signal_delay", 0)

            travel_time = length / mean_speed
            congestion_term = self.lambda_congestion * (queue / capacity)

            total_cost = (
                travel_time
                + congestion_term
                + self.lambda_signal * signal_delay
            )
            self.graph[u][v]["weight"] = total_cost

    def _adaptive_alpha(self, iteration):
        return self.alpha_min + (
            (self.alpha_max - self.alpha_min)
            * iteration / self.num_iterations
        )

    def construct_solution(self, start, end, alpha):
        path = [start]
        visited = set()
        current = start

        while current != end:
            visited.add(current)
            neighbors = list(self.graph.successors(current))
            desirability = []

            for neighbor in neighbors:
                if neighbor in visited:
                    desirability.append(0)
                    continue

                edge = (current, neighbor)
                tau = self.pheromone[edge]
                eta = 1.0 / self.graph[current][neighbor]["weight"]
                desirability.append((tau ** alpha) * (eta ** self.beta))

            if sum(desirability) == 0:
                return None

            probs = np.array(desirability)
            probs /= probs.sum()

            next_node = np.random.choice(neighbors, p=probs)
            path.append(next_node)
            current = next_node

        return path

    def calculate_cost(self, path):
        return sum(
            self.graph[path[i]][path[i+1]]["weight"]
            for i in range(len(path)-1)
        )

    def update_pheromones(self, best_path, best_cost):
        for edge in self.pheromone:
            self.pheromone[edge] *= (1 - self.rho)

        if best_path:
            for i in range(len(best_path)-1):
                edge = (best_path[i], best_path[i+1])
                self.pheromone[edge] += self.Q / best_cost

        for edge in self.pheromone:
            self.pheromone[edge] = np.clip(
                self.pheromone[edge],
                self.tau_min,
                self.tau_max
            )

    def run(self, start, end, traffic_data):
        stagnation = 0

        for iteration in range(self.num_iterations):
            alpha = self._adaptive_alpha(iteration)
            self.update_weights(traffic_data)

            iteration_best_cost = float("inf")
            iteration_best_path = None

            for _ in range(self.num_ants):
                path = self.construct_solution(start, end, alpha)
                if path:
                    cost = self.calculate_cost(path)

                    if cost < iteration_best_cost:
                        iteration_best_cost = cost
                        iteration_best_path = path

            if iteration_best_cost < self.best_global_cost:
                self.best_global_cost = iteration_best_cost
                self.best_global_path = iteration_best_path
                stagnation = 0
            else:
                stagnation += 1

            self.update_pheromones(iteration_best_path, iteration_best_cost)

            if stagnation > 20:
                # restart pheromone partially
                for edge in self.pheromone:
                    self.pheromone[edge] = 1.0
                stagnation = 0

        return self.best_global_path

    def get_edge_path(self, node_path):
        """Converts node sequence to edge sequence for SUMO."""
        if not node_path: return None
        edge_path = []
        for i in range(len(node_path) - 1):
            u = node_path[i]
            v = node_path[i+1]
            edge_path.append(self.graph[u][v]['id'])
        return edge_path

def calculate_optimal_route(start, end, traffic_data, net_file='sumo_sim/grid.net.xml'):
    aco = ACORouting(net_file=net_file)
    node_path = aco.run(start, end, traffic_data)
    return aco.get_edge_path(node_path)



