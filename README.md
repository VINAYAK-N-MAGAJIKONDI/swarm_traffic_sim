# Swarm Traffic Simulation

This project simulates urban traffic using swarm intelligence algorithms (PSO for signal control, ACO for routing) with SUMO and visualizes results in a dashboard.

## Structure
- `sumo_sim/`: SUMO network, routes, and config files
- `controllers/`: PSO and ACO algorithm implementations
- `utils/`: Helper functions for SUMO/TraCI
- `dashboard/`: Streamlit dashboard (optional)
- `results/logs/`: Output data
- `run_simulation.py`: Main script to run the simulation

## Requirements
- Python 3.8+
- SUMO
- TraCI
- Streamlit (optional)

## Usage
1. Edit SUMO files in `sumo_sim/` as needed.
2. Implement/adjust algorithms in `controllers/`.
3. Run the simulation:
   ```bash
   python run_simulation.py
   ```
4. (Optional) Launch dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
