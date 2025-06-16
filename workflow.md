# Swarm Traffic Simulation Project – Workflow Guide

## Overview
This project simulates AI-powered traffic control using Swarm Intelligence algorithms (ACO, PSO, Random, Greedy) with SUMO for traffic simulation and Python for control logic and analytics. The system collects traffic data, optimizes signal timings and vehicle routing, and visualizes results in a dashboard.

---

## Project Flow

1. **SUMO Simulation**
   - SUMO simulates a road network and traffic flow using configuration files.
   - Python (via TraCI) controls and monitors the simulation in real time.

2. **Swarm Intelligence Algorithms**
   - **ACO (Ant Colony Optimization):** Finds optimal vehicle routes based on pheromone trails and traffic conditions.
   - **PSO (Particle Swarm Optimization):** Optimizes traffic signal timings to minimize congestion and wait times.
   - (Optional) **Random/Greedy:** Baseline algorithms for comparison.

3. **Data Collection & Logging**
   - Traffic data (vehicle counts, occupancy, etc.) is collected at each simulation step.
   - Metrics are logged to `results/logs/metrics.csv` for analysis.

4. **Visualization**
   - A Streamlit dashboard visualizes metrics and allows algorithm comparison.

---

## File/Folder Structure & Roles

- **run_simulation.py**
  - Main entry point. Starts SUMO, runs the simulation loop, collects data, calls optimization algorithms, and logs metrics.

- **controllers/**
  - **aco_routing.py:** Implements the ACO algorithm for dynamic vehicle routing. Loads the SUMO network, simulates ant pathfinding, and updates pheromones.
  - **pso_controller.py:** Implements the PSO algorithm for optimizing traffic signal timings.
  - *(Add random/greedy baselines here if needed.)*

- **utils/**
  - **sumo_utils.py:** Utility functions for starting SUMO and retrieving traffic data via TraCI.

- **dashboard/**
  - **app.py:** Streamlit dashboard for visualizing simulation results and comparing algorithms.

- **sumo_sim/**
  - **map.net.xml:** SUMO network file (road map).
  - **routes.rou.xml:** Vehicle routes/trips for the simulation.
  - **simulation.sumocfg:** Main SUMO configuration file linking the map and routes.
  - **traffic.add.xml:** Additional SUMO configuration (e.g., traffic lights).

- **results/logs/**
  - **metrics.csv:** Output metrics from the simulation (created automatically).

- **requirements.txt**
  - Lists all required Python packages.

- **README.md**
  - Project summary, setup, and references.

---

## How Each File Works

- **run_simulation.py**
  - Starts SUMO using `start_sumo()` from `utils/sumo_utils.py`.
  - Initializes ACO and PSO controllers.
  - For each simulation step:
    - Advances SUMO by one step.
    - Collects traffic data.
    - Calls PSO to optimize signal timings.
    - (Optionally) Calls ACO to find optimal routes for vehicles.
    - Logs average vehicle count and occupancy.
  - Saves metrics to `results/logs/metrics.csv`.

- **controllers/aco_routing.py**
  - Loads the SUMO network as a graph using `networkx` and `sumolib`.
  - Implements the ACO algorithm for pathfinding between nodes.
  - Provides a `calculate_optimal_route` function for use in the simulation.

- **controllers/pso_controller.py**
  - Implements a basic PSO algorithm to optimize signal timings based on traffic data.
  - Provides an `optimize_signal_timing` function for use in the simulation.

- **utils/sumo_utils.py**
  - `start_sumo()`: Starts the SUMO simulation with the specified config.
  - `get_traffic_data()`: Collects vehicle count and occupancy for each edge.

- **dashboard/app.py**
  - Loads metrics from `results/logs/metrics.csv`.
  - Displays line and bar charts for metrics.
  - Allows algorithm selection and comparison.

- **sumo_sim/**
  - Contains all SUMO configuration and network files needed to run the simulation.

- **results/logs/**
  - Stores simulation output metrics for analysis and visualization.

---

## How to Run the Project

1. **Install Requirements**
   ```sh
   pip install -r requirements.txt
   ```

2. **Run the Simulation**
   ```sh
   python run_simulation.py
   ```
   - This will start SUMO, run the simulation, and save metrics to `results/logs/metrics.csv`.

3. **View the Dashboard**
   ```sh
   streamlit run dashboard/app.py
   ```
   - Open the provided local URL in your browser to view charts and compare algorithms.

---

## Notes
- Ensure SUMO is installed and available in your system PATH.
- You can switch between SUMO GUI and CLI by changing `SUMO_BINARY` in `run_simulation.py`.
- To add new algorithms, create new files in `controllers/` and update the simulation logic accordingly.
- For custom maps or routes, edit the files in `sumo_sim/`.

---

For further details, see the code comments and the `README.md` file.
