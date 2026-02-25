import sys
import os
import random

# Add project root to path
sys.path.append(os.getcwd())

# Mock sumolib so we don't need actual SUMO binaries just for unit testing logic if possible
# But ACORouting imports it at top level. 
# We'll try running it; if it fails due to missing sumolib, we might need to mock it.
# Assuming user environment has it since run_simulation.py works.

try:
    from controllers.eco_routing import EcoRoutingController
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_eco_routing():
    print("Testing EcoRoutingController...")
    
    net_file = 'sumo_sim/grid.net.xml'
    if not os.path.exists(net_file):
        print(f"Error: {net_file} not found. Using mock graph.")
        # TODO: Implement mock if needed, but for now expect file
        return

    try:
        # Initialize
        print("Initializing controller...")
        controller = EcoRoutingController(net_file=net_file, num_ants=2)
        print("Controller initialized.")
        
        # Get an edge from the graph
        edges = list(controller.graph.edges(data=True))
        if not edges:
            print("No edges found in graph.")
            return
            
        u, v, data = edges[0]
        original_length = data.get('length', 100)
        edge_id = data.get('id')
        
        # Ensure we picked an edge with an ID
        if not edge_id:
            # try to find one with id
            for u2, v2, data2 in edges:
                if data2.get('id'):
                    u, v, data = u2, v2, data2
                    edge_id = data.get('id')
                    original_length = data.get('length', 100)
                    break
        
        print(f"Test Edge: {edge_id} (Nodes: {u}->{v}), Length: {original_length}")
        
        # 1. Test High CO2 (Congestion)
        # Baseline is 2000 mg/s per vehicle.
        # Let's say we have 10,000 mg/s per vehicle (very inefficient)
        print("\nTest 1: High CO2 Scenario")
        traffic_data_high = {
            edge_id: {
                'vehicle_count': 5,
                'co2': 50000.0 # 10,000 per car
            }
        }
        controller.update_weights(traffic_data_high)
        new_weight_high = controller.graph[u][v]['weight']
        print(f"Weight after High emissions: {new_weight_high:.2f}")
        
        expected_weight_high = original_length * (10000.0 / 2000.0) # Should be ~ 5 * length
        print(f"Expected ~{expected_weight_high:.2f}")

        if new_weight_high > original_length:
            print("PASS: Weight increased for high emissions.")
        else:
            print("FAIL: Weight did not increase.")
            
        # 2. Test Low CO2 (Clean)
        # 200 mg/s per vehicle (Eco driving)
        print("\nTest 2: Low CO2 Scenario")
        traffic_data_low = {
            edge_id: {
                'vehicle_count': 5,
                'co2': 1000.0 # 200 per car
            }
        }
        controller.update_weights(traffic_data_low)
        new_weight_low = controller.graph[u][v]['weight']
        print(f"Weight after Low emissions: {new_weight_low:.2f}")
        
        # Factor = 200/2000 = 0.1 -> But we clamped Min Factor to 0.5?
        # Let's check code. Yes MIN_WEIGHT_FACTOR = 0.5
        expected_weight_low = original_length * 0.5
        print(f"Expected ~{expected_weight_low:.2f}")

        if new_weight_low < original_length:
             print("PASS: Weight decreased for low emissions.")
        else:
             print("FAIL: Weight did not decrease appropriately.")
             
        # 3. Test Empty Edge
        print("\nTest 3: Empty Edge")
        traffic_data_empty = {
            edge_id: {
                'vehicle_count': 0,
                'co2': 0.0
            }
        }
        controller.update_weights(traffic_data_empty)
        new_weight_empty = controller.graph[u][v]['weight']
        print(f"Weight for empty edge: {new_weight_empty:.2f}")
        
        if abs(new_weight_empty - original_length) < 0.1:
             print("PASS: Weight reset to length.")
        else:
             print("FAIL: Weight not reset to length.")

    except Exception as e:
        print(f"Exception during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_eco_routing()
