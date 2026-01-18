# Incident Manager Documentation

## Overview
The `IncidentManager` (`utils/incident_manager.py`) simulates traffic accidents or vehicle breakdowns within the SUMO simulation. This allows the user to test the robustness of different traffic control algorithms (like PSO or ACO) under stress conditions.

## How It Works

### Core Logic
The manager tracks the simulation step and triggers an event at a specific time.

1.  **Initialization**: defined in `run_simulation.py`, typically defaulting to:
    -   `start_step`: 200 (Vehicle stops at step 200)
    -   `duration`: 100 (Vehicle remains stopped for 100 steps)
2.  **Triggering (`trigger_incident`)**:
    -   At `start_step`, selects a random vehicle currently in the network.
    -   Sets its speed to **0 m/s**, effectively blocking its lane.
    -   Logs the event to the console: `[INCIDENT] Vehicle <ID> stopped.`
3.  **Clearance (`clear_incident`)**:
    -   After `duration` steps have passed (e.g., step 300), the vehicle is released.
    -   Speed is reset to **-1** (SUMO default, meaning "max allowed speed").
    -   Logs the event to the console: `[INCIDENT CLEARED] Vehicle <ID> released.`

### Robustness
The module includes safety checks to prevent crashes if:
-   The selected vehicle leaves the simulation before the incident ends.
-   No vehicles are present when the incident is supposed to start.

## Output & Visualization

### 1. Console Output
When running `run_simulation.py` in the terminal, you will see direct confirmation of operations:
```text
[INCIDENT] Vehicle 146 stopped.
...
[INCIDENT CLEARED] Vehicle 146 released.
```

### 2. Dashboard (`dashboard/app.py`)
There is no specific "Incident" marker on the dashboard graphs, but the **impact** is clearly visible:
-   **Queue Length Graph**: You will see a sharp spike starting at `start_step` (e.g., step 200) and recovering after the incident clears.
-   **Waiting Time**: Average waiting time will likely increase during this period.
-   **Comparison**: Swarm algorithms (ACO/PSO) should ideally show a *smaller* or *shorter* spike compared to Static algorithms, verifying their adaptability.

### 3. Metric Logs
The raw data is saved to `results/logs/metrics.csv`. You can inspect steps 200–300 to see the exact values for `avg_halting_number` rising.
