# Main script to run the swarm traffic simulation
from controllers.pso_controller import PSOController
from controllers.aco_routing import ACORouting
from utils.sumo_utils import start_sumo, get_traffic_data
import traci
import os
import csv
import subprocess
import webbrowser
import shutil
import time
import sumolib
from xml.etree import ElementTree as ET

SUMO_BINARY = "sumo-gui"  # Use "sumo" for CLI mode
CONFIG = "sumo_sim/simulation.sumocfg"
LOG_FILE = "results/logs/metrics.csv"
SCREENSHOT_DIR = "results/screenshots"
VIDEO_PATH = "results\\video\\simulation.mp4"
DASHBOARD_PATH = "dashboard/app.py"

ALGORITHMS = ["PSO", "ACO"]  # Add more as needed
PARAM_SWEEP = [10]  # Example: number of particles/ants


def cleanup():
    # Remove old screenshots and video
    if os.path.exists(SCREENSHOT_DIR):
        try:
            shutil.rmtree(SCREENSHOT_DIR)
        except PermissionError as e:
            print(f"Could not delete {SCREENSHOT_DIR}: {e}. Please close any programs using this folder and try again.")
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    video_dir = os.path.dirname(VIDEO_PATH)
    if os.path.exists(VIDEO_PATH):
        try:
            os.remove(VIDEO_PATH)
        except PermissionError as e:
            print(f"Could not delete {VIDEO_PATH}: {e}. Please close any programs using this file and try again.")
    os.makedirs(video_dir, exist_ok=True)
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except PermissionError as e:
            print(f"Could not delete {LOG_FILE}: {e}. Please close any programs using this file and try again.")

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

def get_node_from_edge(edge_id, net_file="sumo_sim/map.net.xml", source=True):
    net = sumolib.net.readNet(net_file)
    edge = net.getEdge(edge_id)
    if source:
        return edge.getFromNode().getID()
    else:
        return edge.getToNode().getID()
    
def start_simulation(algorithm="PSO", param=10):
    start_sumo(SUMO_BINARY, CONFIG)
    if algorithm == "PSO":
        controller = PSOController(num_particles=param)
    elif algorithm == "ACO":
        controller = ACORouting(num_ants=param)
    else:
        print(f"Unknown algorithm: {algorithm}")
        return
    metrics = []
    step = 0
    while True:
        traci.simulationStep()
        traffic_data = get_traffic_data()
        if isinstance(controller, PSOController):
            timings = controller.optimize_signal_timing(traffic_data)
        elif isinstance(controller, ACORouting):
            if step == 0:
            
                # Use the first trip from map.rou.xml as an example
                trips = ET.parse("sumo_sim/map.rou.xml").findall("trip")
                if trips:
                    from_edge = trips[0].attrib["from"]
                    to_edge = trips[0].attrib["to"]
                    start_node = get_node_from_edge(from_edge, source=True)
                    end_node = get_node_from_edge(to_edge, source=False)
                    route = controller.run(start_node, end_node)
                    print(f"ACO route from {start_node} to {end_node}: {route}")
                else:
                    print("No trips found in map.rou.xml")
        avg_vehicles = sum([v['vehicle_count'] for v in traffic_data.values()]) / len(traffic_data)
        avg_occupancy = sum([v['occupancy'] for v in traffic_data.values()]) / len(traffic_data)
        metrics.append({'step': step, 'avg_vehicles': avg_vehicles, 'avg_occupancy': avg_occupancy, 'algorithm': algorithm, 'param': param})
        if step % 50 == 0:
            screenshot_path = os.path.join(SCREENSHOT_DIR, f"{algorithm}_{param}_step_{step:04d}.png")
            try:
                traci.gui.screenshot(viewID='View #0', filename=screenshot_path)
            except Exception as e:
                print(f"Screenshot failed at step {step}: {e}")
        step += 1
        # Stop if all vehicles have arrived
        if traci.simulation.getMinExpectedNumber() == 0:
            print("All vehicles have arrived. Stopping simulation.")
            break
    traci.close()
    # Save metrics
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    write_header = not os.path.exists(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['step', 'avg_vehicles', 'avg_occupancy', 'algorithm', 'param'])
        if write_header:
            writer.writeheader()
        writer.writerows(metrics)
    print(f"Simulation complete for {algorithm} (param={param}). Metrics saved.")

def parameter_sweep():
    for algo in ALGORITHMS:
        for param in PARAM_SWEEP:
            print(f"Running {algo} with param={param}")
            start_simulation(algorithm=algo, param=param)
            time.sleep(2)  # Give SUMO time to close

def main():
    cleanup()
    parameter_sweep()
    run_ffmpeg()
    generate_report()
    check_errors()
    launch_dashboard()

if __name__ == "__main__":
    main()
