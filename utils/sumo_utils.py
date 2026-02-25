# SUMO TraCI helper functions
# Add utility functions to interact with SUMO via TraCI
import traci
import traci.constants as tc

def start_sumo(sumo_binary='sumo', config='sumo_sim/simulation.sumocfg'):
    traci.start([sumo_binary, '-c', config])

def get_traffic_data():
    # Example: collect vehicle count and edge occupancy
    edge_ids = traci.edge.getIDList()
    traffic_data = {
        '__network__': {
            'teleports': traci.simulation.getStartingTeleportNumber(),
            'throughput': traci.simulation.getArrivedNumber()
        }
    }
    for edge in edge_ids:
        # Signal Delay Heuristic: 1 if leading to a RED light, 0 otherwise
        signal_delay = 0
        try:
            # Check the state of the first link if it's controlled by a TLS
            # This is a simplified check for signal delay integration
            links = traci.edge.getLanes(edge)
            if links:
                lane_id = links[0]
                tls_links = traci.trafficlight.getControlledLinks(traci.lane.getEdgeID(lane_id))
                # This check is complex with pure TraCI, simplified heuristic:
                # If the mean speed is very low but occupancy is high, and it's near a junction...
                # Actually, TraCI doesn't easily give "is this edge currently red" without 
                # mapping lane to TLS phase index. 
                # Better heuristic for IEEE ACO: signal_delay = 1.0 if mean_speed < 1.0 and vehicle_count > 0
                if traci.edge.getLastStepMeanSpeed(edge) < 1.0 and traci.edge.getLastStepVehicleNumber(edge) > 0:
                    signal_delay = 1.0
        except Exception:
            pass

        traffic_data[edge] = {
            'vehicle_count': traci.edge.getLastStepVehicleNumber(edge),
            'occupancy': traci.edge.getLastStepOccupancy(edge),
            'waiting_time': traci.edge.getWaitingTime(edge),
            'halting_number': traci.edge.getLastStepHaltingNumber(edge),
            'mean_speed': traci.edge.getLastStepMeanSpeed(edge),
            'co2': traci.edge.getCO2Emission(edge),
            'length': traci.lane.getLength(edge + "_0") if traci.edge.getLaneNumber(edge) > 0 else 100,
            'signal_delay': signal_delay
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
