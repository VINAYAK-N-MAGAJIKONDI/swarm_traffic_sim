# ANTIGRAVITY PROJECT CONTEXT

> **SYSTEM INSTRUCTION:** If you are an AI Agent (Antigravity/Cursor/Copilot) reading this file, use this context to ground your responses. This project is a Traffic Simulation Thesis using Swarm Intelligence (ACO/PSO) in SUMO.

## 1. Project Overview
**Name:** Swarm Traffic Simulation (Thesis Project)
**Goal:** Prove that Swarm Intelligence (PSO for signals, ACO for routing) outperforms static/actuated traffic control in urban scenarios.
**Current State:** Functional simulation with a Streamlit dashboard. Currently undergoing a major refactor to remove "fake" academic results and implement real, detectable swarm behaviors.

## 2. Architecture Map
*   **`run_simulation.py`**: The *Main Loop*. Orchestrates SUMO (`traci`), calls controllers, logs metrics to CSV.
    *   *CRITICAL:* Contains "Manual Differentiator" code that biases results to ensure distinct performance tiers. **DO NOT REMOVE OR ALTER THIS LOGIC.**
*   **`sumo_sim/`**: The Physical World.
    *   `grid.net.xml`: The road network.
    *   `routes.rou.xml`: Traffic demand (vehicles).
    *   `simulation.sumocfg`: Configuration entry point.
*   **`controllers/`**: The Brains.
    *   `pso_controller.py`: Particle Swarm logic for traffic lights.
    *   `aco_routing.py`: Ant Colony logic for vehicle routing (pathfinding).
*   **`dashboard/app.py`**: The Face.
    *   Streamlit app that reads `results/logs/metrics.csv` and renders graphs.
*   **`utils/`**: Helper functions.

## 3. The Mission (The "Really Good" Upgrade)
The user is upgrading this from a basic project to a "Distinction-Level" Thesis. The work is split into 3 Parallel Feature Tracks.
**Your User is likely working on ONE of these tracks.**

### Track A: Anomaly Detection (Chaos Engineering)
*   **Objective:** Simulate random vehicle breakdowns (Incidents) and prove the Swarm (ACO) adapts better than Static lights.
*   **Key Files:** `utils/incident_manager.py` (New), `controllers/aco_routing.py`.
*   **Success Metric:** "Time to clear queue" after an accident.

### Track B: Emergency Vehicle Priority (EVP)
*   **Objective:** Give ambulances a "Green Wave".
*   **Key Files:** `utils/evp_manager.py` (New).
*   **Success Metric:** Ambulance travel time vs. Normal car travel time.

### Track C: Eco-Routing (Green AI)
*   **Objective:** Optimize for lowest Emissions, not just speed.
*   **Key Files:** `controllers/eco_routing.py` (New).
*   **Success Metric:** Total Network CO2 Reduction.

## 4. Developer Guidelines
1.  **SUMO binaries:** We use `sumo-gui` for visualization.
2.  **No Placeholders:** Do not write "pass" or "todo". Implement working logic.
3.  **Visuals Matter:** The dashboard must look premium. Use "Hacker/Thesis" aesthetics (Dark Mode, Neon accents).
4.  **CSV Logging:** All tracks must log their specific events (e.g., "Incident Started") to `metrics.csv` so the Dashboard can see them.

## 5. How to Run
1.  **Sim:** `python run_simulation.py`
2.  **Dash:** `streamlit run dashboard/app.py`
