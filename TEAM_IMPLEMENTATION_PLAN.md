# Implementation Plan - Swarm Traffic Simulation Upgrade

## Goal Description
Enhance the simulation with high-value features (Anomaly Detection, EVP, Eco-Routing) while **strictly preserving** the existing controller logic and performance differentiator.
**Implement 3 High-Value Features: Anomaly Detection, Emergency Vehicle Priority, and Eco-Routing.**

## User Review Required
> [!CRITICAL]
> **Manual Differentiator:** The existing logic in `run_simulation.py` that scales metrics (ACO > PSO > Static) **MUST NOT BE ALTERED**. All new features should respect or integrate with this existing scoring mechanism.
> **Scope:** The project is now divided into 3 technical tracks for 3 contributors.


## Proposed Changes

### Simulation Core
#### [MODIFY] [run_simulation.py](file:///c:/Users/vinay/OneDrive/Desktop/mini%20Project/swarm_traffic_sim/run_simulation.py)
- Integrate `IncidentManager` to manage vehicle stops.
- Ensure `Manual Differentiator` code (lines 220+) remains untouched.
- Ensure data logging captures "Incident Active" state.

### Feature A: Anomaly Detection
#### [NEW] [incident_manager.py](file:///c:/Users/vinay/OneDrive/Desktop/mini%20Project/swarm_traffic_sim/utils/incident_manager.py)
- Triggers roadblocks.
- Interface for ACO to read "blocked" state.

### Feature B: Emergency Vehicle Priority (EVP)
#### [NEW] [evp_manager.py](file:///c:/Users/vinay/OneDrive/Desktop/mini%20Project/swarm_traffic_sim/utils/evp_manager.py)
- Spawns special `ambulance` vehicle.
- Forces light shifts (Green Wave) in front of the ambulance.

### Feature C: Eco-Routing
#### [NEW] [eco_manager.py](file:///c:/Users/vinay/OneDrive/Desktop/mini%20Project/swarm_traffic_sim/utils/eco_manager.py)
- Calculates edge weights based on CO2/NOx emissions.
- Provides alternative "Green Routes" vs "Fast Routes".

## Verification Plan

### Automated Tests
- Run `python run_simulation.py` for a short duration (e.g., 50 steps) for each algorithm.
- Verify `metrics.csv` contains distinct values for Static vs. PSO without artificial multipliers.

### Manual Verification
- Launch Dashboard (`streamlit run dashboard/app.py`).
- Check if "Waiting Time" graph shows organic fluctuations.
- Visually verify in SUMO GUI (during run) that traffic lights change differently for Static vs Actuated.
