# SUMO TraCI helper functions
# Add utility functions to interact with SUMO via TraCI
import traci
import traci.constants as tc

def start_sumo(sumo_binary='sumo', config='sumo_sim/simulation.sumocfg'):
    traci.start([sumo_binary, '-c', config])

def get_traffic_data():
    # Example: collect vehicle count and edge occupancy
    edge_ids = traci.edge.getIDList()
    traffic_data = {}
    for edge in edge_ids:
        traffic_data[edge] = {
            'vehicle_count': traci.edge.getLastStepVehicleNumber(edge),
            'occupancy': traci.edge.getLastStepOccupancy(edge),
            'waiting_time': traci.edge.getWaitingTime(edge),
            'halting_number': traci.edge.getLastStepHaltingNumber(edge),
            'co2': traci.edge.getCO2Emission(edge)
        }
    return traffic_data

def apply_signal_timings(timings, edge_ids):
    """
    Apply optimized timings to traffic lights.
    Note: Maps edge_id -> TLS via TraCI.
    """
    # This is a heuristic mapping since pso operates on edges
    # We try to find the TLS controlling the node at the end of the edge
    for i, edge in enumerate(edge_ids):
        timing = timings[i]
        try:
            # Check if this edge feeds into a traffic light
            # In TraCI there isn't a direct "getTLS" for an edge without sumolib
            # So we iterate all TLS and see if they control this edge's lanes
            # Optimization: This is slow (O(N*M)). 
            # Better approach for Final Project: PSO should optimize TLS IDs, not edges.
            # For now, we apply to any TLS found interacting with the edge.
            pass 
        except Exception:
            pass
            
    # BETTER IMPLEMENTATION for Phased Project:
    # Just iterate valid traffic lights and apply values from the 'particles' 
    # assuming particles[i] maps to tls_list[i].
    
    tls_ids = traci.trafficlight.getIDList()
    # If the PSO vector is larger/smaller, we truncate or loop
    count = len(timings)
    for i, tls in enumerate(tls_ids):
        if i < count:
            # Set the current phase duration to the optimized value
            # This extends/shortens the CURRENT green light
            try:
                traci.trafficlight.setPhaseDuration(tls, timings[i])
            except traci.exceptions.TraCIException:
                pass
