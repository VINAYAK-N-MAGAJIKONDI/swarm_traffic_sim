# Main script to run the swarm traffic simulation
from controllers.pso_controller import PSOController
from controllers.aco_routing import ACORouting
from controllers.eco_routing import EcoRoutingController
from utils.sumo_utils import start_sumo, get_traffic_data
from utils.incident_manager import IncidentManager
import traci
import os
import csv
import subprocess
import webbrowser
import shutil
import time
import sumolib
import random
from xml.etree import ElementTree as ET

SUMO_BINARY = "sumo-gui"  # Use "sumo" for CLI mode
# Simulation Mode: "Quick" (Faster, Realistic) or "Strain" (Original, Intensive)
SIM_MODE = "Quick" 

if SIM_MODE == "Quick":
    CONFIG = "sumo_sim/quick_simulation.sumocfg"
else:
    CONFIG = "sumo_sim/simulation.sumocfg"

LOG_FILE = "results/logs/metrics.csv"
SCREENSHOT_DIR = "results/screenshots"
VIDEO_PATH = "results\\video\\simulation.mp4"
DASHBOARD_PATH = "dashboard/app.py"

ALGORITHMS = ["Static", "Actuated", "PSO", "ACO", "Eco"]  # Add more as needed
# Default parameter for PSO/ACO/Eco
DEFAULT_PARAM = 10 



def cleanup():
    # Remove old screenshots and video
    for path in [SCREENSHOT_DIR, LOG_FILE]:
        if os.path.exists(path):
            for i in range(3): # Retry logic for Windows file locks
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    break
                except PermissionError:
                    time.sleep(1)
    
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    video_dir = os.path.dirname(VIDEO_PATH)
    os.makedirs(video_dir, exist_ok=True)


def run_ffmpeg():
    # Create video from screenshots
    cmd = [
        "ffmpeg", "-y", "-framerate", "10", "-i",
        os.path.join(SCREENSHOT_DIR, "step_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", VIDEO_PATH
    ]
    print("Running ffmpeg command:", ' '.join(cmd))
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("ffmpeg stdout:\n", result.stdout)
        print("ffmpeg stderr:\n", result.stderr)
        print("Video created at", VIDEO_PATH)
    except subprocess.CalledProcessError as e:
        print("Video creation failed:", e)
        print("ffmpeg stdout:\n", e.stdout)
        print("ffmpeg stderr:\n", e.stderr)
    except Exception as e:
        print("Video creation failed (unexpected error):", e)

def launch_dashboard():
    # Launch Streamlit dashboard
    try:
        webbrowser.open_new_tab(f"http://localhost:8501")
        subprocess.Popen(["streamlit", "run", DASHBOARD_PATH])
        print("Dashboard launched.")
    except Exception as e:
        print("Dashboard launch failed:", e)

def generate_report():
    # Simple markdown report
    report_path = "results/report.md"
    try:
        with open(LOG_FILE) as f:
            lines = f.readlines()
        with open(report_path, "w") as f:
            f.write("# Simulation Report\n\n")
            f.write(f"Algorithm: {ALGORITHMS}\n\n")
            f.write("## Metrics (first 10 steps):\n\n")
            f.writelines(lines[:11])
        print("Report generated at", report_path)
    except Exception as e:
        print("Report generation failed:", e)

def check_errors():
    # Check for common SUMO/TraCI errors in log file
    if os.path.exists("sumo_sim/sumo.log"):
        with open("sumo_sim/sumo.log") as f:
            log = f.read()
        if "invalid document structure" in log:
            print("ERROR: Invalid XML structure in SUMO config files.")
        if "edge" in log and "not known" in log:
            print("ERROR: Route references unknown edge. Check your routes.rou.xml.")

def get_node_from_edge(edge_id, net_file="sumo_sim/grid.net.xml", source=True):
    net = sumolib.net.readNet(net_file)
    edge = net.getEdge(edge_id)
    if source:
        return edge.getFromNode().getID()
    else:
        return edge.getToNode().getID()
    

from utils.benchmark_stats import BenchmarkStats

def start_simulation(algorithm="PSO", param=10, benchmark_stats=None):
    # Robust start with retries
    for i in range(3):
        try:
            start_sumo(SUMO_BINARY, CONFIG)
            break
        except Exception as e:
            print(f"Start attempt {i+1} failed: {e}. Retrying...")
            time.sleep(2)
    
    incident_manager = IncidentManager(start_step=200, duration=100)

    
    # DEBUG
    print("Simulation started.")
    print(f"Loaded Routes: {traci.route.getIDList()[:5]}")
    print(f"Traffic Lights: {traci.trafficlight.getIDList()}")
    
    controller = None
    
    if algorithm == "PSO":
        controller = PSOController(num_particles=param)
    elif algorithm == "ACO":
        controller = ACORouting(num_ants=param)
    elif algorithm == "Eco":
        controller = EcoRoutingController(num_ants=param)
    elif algorithm == "Static":
        # Static Timing: Do nothing, let SUMO use default net.xml phases
        pass
    elif algorithm == "Actuated":
        # Actuated: For now, we simulate this by doing nothing if the map has actuated lights,
        # or we could stick to default. For this project, we treat "default map logic" as one baseline.
        # If we want distinct Static vs Actuated, we would need to load different .net.xml files or 
        # use TraCI to switch TLS programs. 
        # For simplicity: We will assume "Static" is default, and "Actuated" runs a simple gap-logic here if we wanted.
        # But for now let's just use Default as "Static" and maybe "Actuated" as a placeholder for future.
        pass
    else:
        print(f"Unknown algorithm: {algorithm}")
        return

    metrics = []
    
    # Define fields for CSV
    fieldnames = ['step', 'avg_vehicles', 'avg_occupancy', 'avg_waiting_time', 'avg_halting_number', 'avg_co2', 'algorithm', 'param']
    
    step = 0
    while True:
        try:
            traci.simulationStep()
            incident_manager.update(step)
            traffic_data = get_traffic_data()
        except traci.exceptions.FatalTraCIError:
            print("Simulation ended (connection lost).")
            break

        if isinstance(controller, PSOController):
            timings = controller.optimize_signal_timing(traffic_data)
            # Actuation
            from utils.sumo_utils import apply_signal_timings
            edge_ids = list(traffic_data.keys())
            apply_signal_timings(timings, edge_ids)
            
        elif isinstance(controller, ACORouting):
            # Dynamic ACO logic is handled inside if we had it fully integrated 
            # (previous step added check for isinstance ACORouting)
             # Dynamic Rerouting every 50 steps
            if step % 50 == 0:
                controller.update_weights(traffic_data)
                
                # Reroute a subset of vehicles
                veh_ids = traci.vehicle.getIDList()
                # import random # Removed local import to avoid shadowing global
                for veh_id in veh_ids:
                    if random.random() < 0.1: # 10%
                        try:
                            road_id = traci.vehicle.getRoadID(veh_id)
                            if road_id.startswith(":"): continue
                            route = traci.vehicle.getRoute(veh_id)
                            if not route: continue
                            target_edge = route[-1]
                            start_node = get_node_from_edge(road_id, source=False)
                            end_node = get_node_from_edge(target_edge, source=False)
                            if start_node and end_node and start_node != end_node:
                                node_path = controller.run(start_node, end_node, traffic_data)
                                edge_path = controller.get_edge_path(node_path)
                                if edge_path:
                                    try:
                                        traci.vehicle.setRoute(veh_id, edge_path)
                                    except traci.exceptions.TraCIException:
                                        pass # Route might be invalid or vehicle moved
                        except Exception:
                            pass

        
        # Calculate Network-wide Stats safely
        edge_data = {k: v for k, v in traffic_data.items() if k != '__network__'}
        count = len(edge_data)
        if count > 0:
            avg_vehicles = sum(d['vehicle_count'] for d in edge_data.values()) / count
            avg_occupancy = sum(d['occupancy'] for d in edge_data.values()) / count
            avg_waiting_time = sum(d.get('waiting_time', 0) for d in edge_data.values()) / count
            avg_halting_number = sum(d.get('halting_number', 0) for d in edge_data.values()) / count
            avg_co2 = sum(d.get('co2', 0) for d in edge_data.values()) / count

        else:
            avg_vehicles = avg_occupancy = avg_waiting_time = avg_halting_number = avg_co2 = 0


        # ---------------------------------------------

        metric_step = {
            'step': step, 
            'avg_vehicles': avg_vehicles, 
            'avg_occupancy': avg_occupancy, 
            'avg_waiting_time': avg_waiting_time,
            'avg_halting_number': avg_halting_number,
            'avg_co2': avg_co2,
            'algorithm': algorithm, 
            'param': param
        }
        metrics.append(metric_step)
        
        # Write immediately to CSV to prevent data loss on crash/close
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        file_exists = os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0
        try:
            with open(LOG_FILE, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(metric_step)
        except PermissionError:
            print("Warning: Could not write to log file (permission denied).")
        
        if step % 50 == 0:
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{algorithm}_{param}_step_{step:04d}.png")
            try:
                traci.gui.screenshot(viewID='View #0', filename=screenshot_path)
            except Exception as e:
                print(f"Screenshot failed at step {step}: {e}")
        step += 1
        # Stop if all vehicles have arrived
        if traci.simulation.getMinExpectedNumber() == 0:
            print(f"All vehicles have arrived at step {step}. Stopping simulation.")
            break
            
    if step == 0:
        print("WARNING: Simulation ran for 0 steps!")
            
    traci.close()
    
    # Save metrics to CSV
    # Save metrics to CSV - (Already done in loop, but ensuring benchmark stats work)
    # Removing bulk write to avoid duplicates if we wrote in loop.
    # But we need to ensure header is there if loop didn't run.
    if not os.path.exists(LOG_FILE):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
    
    print(f"Simulation complete for {algorithm} (param={param}). Metrics saved.")
    
    if benchmark_stats:
        benchmark_stats.add_run(algorithm, param, metrics)

def run_benchmarks():
    stats = BenchmarkStats()
    
    for algo in ALGORITHMS:
        param = 0 if algo in ["Static", "Actuated"] else DEFAULT_PARAM
        print(f"--- Running {algo} ---")
        start_simulation(algorithm=algo, param=param, benchmark_stats=stats)
        time.sleep(2) # Stabilize SUMO closing
    
    stats.print_summary()


def main():
    cleanup()
    run_benchmarks()
    run_ffmpeg()
    generate_report()
    check_errors()
    launch_dashboard()

if __name__ == "__main__":
    main()
