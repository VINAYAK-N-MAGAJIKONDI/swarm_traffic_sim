import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.getcwd())

from controllers.pso_controller import PSOController

def test_pso_logic():
    print("Testing ResearchGradePSO logic...")
    
    controller = PSOController(num_particles=5, num_iterations=10)
    
    # Test 1: Normal Optimization
    print("Test 1: Normal Optimization...")
    traffic_data_normal = {
        'edge1': {'waiting_time': 100, 'halting_number': 10, 'length': 200},
        'edge2': {'waiting_time': 50, 'halting_number': 2, 'length': 200},
        '__network__': {'teleports': 0, 'throughput': 10}
    }
    best_timings = controller.optimize_signal_timing(traffic_data_normal)
    print(f"Best Timings: {best_timings}")
    if abs(np.sum(best_timings) - 120.0) < 0.1:
        print("PASS: Cycle normalization works.")
    
    # Test 2: Teleport Penalty
    print("\nTest 2: Teleport Penalty Logic...")
    # A plan with teleports should have a massive score
    def mock_sim_teleport(timings):
        return {"total_delay": 0, "total_queue": 0, "teleports": 5, "throughput": 0, "spillback": 0}
    
    score = controller.fitness([30, 30], mock_sim_teleport)
    print(f"Teleport Score: {score}")
    if score >= 1e12:
        print("PASS: Teleport penalty triggered.")
    else:
        print("FAIL: Teleport penalty failed.")

        
    if len(best_timings) == 2:
        print("PASS: Correct dimension handled.")
    else:
        print("FAIL: Dimension mismatch.")

if __name__ == "__main__":
    test_pso_logic()
