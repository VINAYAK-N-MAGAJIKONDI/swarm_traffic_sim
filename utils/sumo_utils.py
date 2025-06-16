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
            'occupancy': traci.edge.getLastStepOccupancy(edge)
        }
    return traffic_data
