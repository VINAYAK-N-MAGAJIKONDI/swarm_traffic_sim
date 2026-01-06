# Swarm Traffic Simulation - Feature-Based Team Task List

## Track A: Anomaly Detection & Incident Response (Person 1) <!-- id: 0 -->
**Goal:** Simulate accidents and have the Swarm automatically reroute traffic.
- [ ] **Incident Simulation** <!-- id: 1 -->
    - [ ] Create `utils/incident_manager.py` to trigger vehicle breakdowns (speed=0) <!-- id: 2 -->
    - [ ] Visualize "Blocked" edges in the simulation (color change) <!-- id: 3 -->
- [ ] **Swarm Reaction** <!-- id: 4 -->
    - [ ] Update ACO logic to detect "blocked" edges (infinite cost) <!-- id: 5 -->
    - [ ] Demonstrate queue dissipation after rerouting <!-- id: 6 -->

## Track B: Emergency Vehicle Priority (EVP) (Person 2) <!-- id: 7 -->
**Goal:** Ambulances move through traffic faster using Swarm/V2I communication.
- [ ] **Ambulance Agent** <!-- id: 8 -->
    - [ ] Define a new vehicle type `ambulance` in SUMO <!-- id: 9 -->
    - [ ] Create `utils/evp_manager.py` to track ambulance position <!-- id: 10 -->
- [ ] **Signal Preemption** <!-- id: 11 -->
    - [ ] Override traffic lights to GREEN when ambulance approaches <!-- id: 12 -->
    - [ ] Measure "Time to Hospital" metric vs normal traffic <!-- id: 13 -->

## Track C: Eco-Routing & Green Waves (Person 3) <!-- id: 14 -->
**Goal:** Optimize traffic not just for speed, but to minimize CO2 emissions.
- [ ] **Emission Monitoring** <!-- id: 15 -->
    - [ ] Utilize SUMO's emission models (HBEFA) to track real-time pollution <!-- id: 16 -->
    - [ ] Create `controllers/eco_routing.py` <!-- id: 17 -->
- [ ] **Eco-Weighting** <!-- id: 18 -->
    - [ ] Route vehicles via "Cleanest" path, not just "Fastest" <!-- id: 19 -->
    - [ ] Verify reduction in total network CO2 <!-- id: 20 -->
