import networkx as nx
from controllers.aco_routing import ACORouting

class EcoRoutingController(ACORouting):
    """
    Eco-Routing Controller using Ant Colony Optimization.
    Optimizes for minimal CO2 emissions (HBEFA model) instead of travel time.
    """
    def __init__(self, net_file='sumo_sim/grid.net.xml', num_ants=10, num_iterations=50, alpha=1, beta=3, rho=0.5, q=1.0):
        super().__init__(net_file, num_ants, num_iterations, alpha, beta, rho, q)

    def update_weights(self, traffic_data):
        """
        Dynamically update graph weights based on real-time CO2 emissions.
        
        Weight Formula:
        If Edge has vehicles:
            Avg_CO2_Rate = Total_Edge_CO2 / Vehicle_Count
            Weight = Length * (Avg_CO2_Rate / Baseline_Rate)
        If Edge is empty:
            Weight = Length (Baseline assumptions)
            
        This penalizes edges where vehicles are currently emitting high levels of CO2
        (e.g. stop-and-go traffic, high acceleration).
        """
        BASELINE_CO2_RATE = 2000.0  # mg/s (heuristic for a moving vehicle)
        MIN_WEIGHT_FACTOR = 0.5     # Don't let weight drop too low (e.g. idling cars)

        for u, v, data in self.graph.edges(data=True):
            edge_id = data.get("id")
            if edge_id and edge_id in traffic_data:
                edge_stats = traffic_data[edge_id]
                
                # Fetch Real-time HBEFA CO2 emissions for the edge (total mg/s for all vehs)
                total_co2 = edge_stats.get("co2", 0.0) 
                veh_count = edge_stats.get("vehicle_count", 0)
                length = data.get("original_length", 100.0) # meters
                
                new_weight = length # Default to length if no info

                if veh_count > 0:
                    # Calculate average emission rate per vehicle on this edge
                    avg_co2_rate = total_co2 / veh_count
                    
                    # Normalize against a baseline "acceptable" emission
                    # If avg_co2_rate > 2000, ratio > 1, weight > length (Penalty)
                    # If avg_co2_rate < 2000, ratio < 1, weight < length (Reward - e.g. coasting/idling efficiently?)
                    # Note: We enforce a min factor to prevent infinite loops or zero-cost edges
                    co2_factor = max(avg_co2_rate / BASELINE_CO2_RATE, MIN_WEIGHT_FACTOR)
                    
                    new_weight = length * co2_factor
                else:
                    # Empty edge: Valid assumption is it allows "Baseline" efficient driving
                    new_weight = length * 1.0

                # Update graph weight
                self.graph[u][v]["weight"] = new_weight
