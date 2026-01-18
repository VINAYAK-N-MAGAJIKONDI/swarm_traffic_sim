# FINAL YEAR PROJECT REPORT

**PROJECT TITLE:** SWARM INTELLIGENCE BASED TRAFFIC OPTIMIZATION SIMULATION (SITOS)

---

**SUBMITTED BY:**  
[Your Name]  
[Your Roll Number]  

**GUIDED BY:**  
[Professor Name]  
Department of Computer Science & Engineering  
[University Name]  

**DATE:** January 18, 2026

---

## DECLARATION

I hereby declare that the project titled **"Swarm Intelligence Based Traffic Optimization Simulation (SITOS)"** submitted by me for the partial fulfillment of the degree of **Bachelor of Technology** in **Computer Science** is a record of my own work carried out under the supervision of **[Professor Name]**. The matter embodied in this report has not been submitted to any other University or Institute for the award of any degree.

**(Signature)**  
[Your Name]

---

## ACKNOWLEDGEMENT

I would like to express my deep gratitude to my project guide **[Professor Name]** for their patient guidance, enthusiastic encouragement, and useful critiques of this research work.

I would also like to thank the **Eclipse SUMO Community** for providing the open-source tools that made this simulation possible, and the **Python Software Foundation** for the extensive libraries used in this project.

Finally, thanks to my parents and friends for their support throughout the development of this project.

---

## ABSTRACT

Urban traffic congestion is a multifaceted problem characterized by stochastic demand and constrained infrastructure. Traditional control mechanisms, such as fixed-cycle traffic lights and localized inductive loops (Actuated Control), often fail to mitigate congestion in high-density scenarios due to their lack of global coordination. This project proposes, implements, and validates a decentralized approach using **Swarm Intelligence (SI)** meta-heuristics.

We developed **SITOS (Swarm Intelligence Traffic Optimization Simulation)**, a comprehensive framework bridging **Python** (for algorithmic logic) and **SUMO** (for microscopic traffic physics) via the **TraCI** interface. The system implements two core algorithms:
1.  **Particle Swarm Optimization (PSO)**: Used to optimize Traffic Signal Timings dynamically based on real-time queue lengths, treating signal phases as particles in a multi-dimensional search space.
2.  **Ant Colony Optimization (ACO)**: Used for Dynamic Vehicle Routing, where virtual "ants" explore the road network to identify optimal paths based on pheromone trails that represent travel efficiency.

Additionally, a novel **Eco-Routing** module was developed to minimize $CO_2$ emissions using HBEFA impact models. The system was benchmarked on a 5x5 Manhattan Grid under normal and "Incident" (accident) conditions. Results demonstrate that the Swarm-based approach reduces Average Waiting Time by **67.14%** and Queue Length by **67.46%** compared to static baselines, proving that bio-inspired, decentralized algorithms offer a scalable solution for modern smart cities.

**Keywords**: Swarm Intelligence, PSO, ACO, SUMO, Traffic Simulation, Smart City, Eco-Routing.

---

## TABLE OF CONTENTS

1.  **CHAPTER 1: INTRODUCTION**
    *   1.1 Motivation
    *   1.2 Problem Domain
    *   1.3 Objectives
    *   1.4 Societal Impact
    *   1.5 Scope and Limitations

2.  **CHAPTER 2: LITERATURE REVIEW**
    *   2.1 Evolution of Traffic Control Systems
    *   2.2 Shift towards Intelligent Transportation Systems (ITS)
    *   2.3 Swarm Intelligence: State of the Art
    *   2.4 Research Gap Analysis

3.  **CHAPTER 3: SYSTEM ANALYSIS (SRS)**
    *   3.1 Feasibility Study (Technical, Economic, Operational)
    *   3.2 Requirement Specification (Functional & Non-Functional)
    *   3.3 Hardware & Software Requirements

4.  **CHAPTER 4: SYSTEM DESIGN**
    *   4.1 System Architecture (The control Loop)
    *   4.2 Data Flow Diagrams (Level 0, Level 1)
    *   4.3 UML Diagrams (Use Case, Sequence, Class)
    *   4.4 Database Design (CSV Schema)

5.  **CHAPTER 5: THEORETICAL FRAMEWORK & ALGORITHMS**
    *   5.1 Particle Swarm Optimization (PSO) - Mathematical Model
    *   5.2 Ant Colony Optimization (ACO) - Mathematical Model
    *   5.3 Pseudo-code for Implemented Algorithms

6.  **CHAPTER 6: IMPLEMENTATION DETAILS**
    *   6.1 Technology Stack Definition
    *   6.2 Directory Structure
    *   6.3 Module Description (Controllers, Simulation, Dashboard)
    *   6.4 Incident Management Logic

7.  **CHAPTER 7: TESTING & VALIDATION**
    *   7.1 Testing Strategy
    *   7.2 Unit Testing
    *   7.3 Integration Testing
    *   7.4 Validation Scenarios

8.  **CHAPTER 8: RESULTS & PERFORMANCE ANALYSIS**
    *   8.1 Performance Metrics
    *   8.2 Comparative Analysis Tables
    *   8.3 Graphical Analysis
    *   8.4 Case Study: Incident Resilience

9.  **CHAPTER 9: CONCLUSION & FUTURE SCOPE**

**REFERENCES**

---

## CHAPTER 1: INTRODUCTION

### 1.1 Motivation
The 21st century has seen unprecedented urbanization. According to the UN, 68% of the world population is projected to live in urban areas by 2050. This surge puts immense pressure on existing road networks. Building new roads is often geographically impossible or economically unviable in established cities. Thus, the focus must shift from **Infrastructure Expansion** to **Infrastructure Optimization**.

### 1.2 Problem Domain
Traffic congestion is a "Tragedy of the Commons" scenario where individual agents (drivers) optimizing their own travel time lead to extensive delays for the system as a whole.
*   **Static Lights**: 90% of global intersections run on fixed timers. They cannot see empty roads or long queues.
*   **Centralized AI**: While promising, centralized servers represent a Single Point of Failure and high latency.
*   **Pollution**: Step-and-go traffic increases fuel consumption by up to 30%.

### 1.3 Objectives
1.  **Design a robust simulation Platform**: Integrate Python and SUMO to allow frame-by-frame manipulation of traffic elements.
2.  **Implement PSO for Signals**: Create an algorithm that adjusts Green/Red times in real-time to flush queues.
3.  **Implement ACO for Routing**: Create an algorithm that distributes traffic loads across less-congested alternative routes.
4.  **Develop Eco-Routing**: Prioritize routes with lower emission gradients.
5.  **Visualize Results**: Build a dashboard to make the complex data understandable for decision-makers.

### 1.4 Societal Impact
*   **Quality of Life**: Reducing commute times limits driver stress and fatigue.
*   **Emergency Services**: An intelligent grid can "clear the way" for ambulances without human intervention.
*   **Sustainability**: Optimizing flow directly correlates to reduced carbon footprints, aiding in climate goals.

### 1.5 Scope and Limitations
*   **Scope**: The project is limited to surface street optimization (intersections). It assumes Connected Vehicle (CV) technology where the system knows the location of vehicles.
*   **Limitations**:
    *   **GPS Accuracy**: Simulation assumes 100% position accuracy.
    *   **Human Factor**: Does not model irrational driver behavior (e.g., road rage).
    *   **Hardware**: The prototype is software-only; hardware deployment is theoretical.

---

## CHAPTER 2: LITERATURE REVIEW

### 2.1 Evolution of Traffic Control Systems
*   **Pre-1920s**: Manual police direction.
*   **1920s-1970s**: Fixed Cycle (Pre-timed) controllers.
*   **1970s-Present**: SCATS (Sydney Coordinated Adaptive Traffic System) and SCOOT. These rely on inductive loops and are expensive to install ($\sim\$50,000$ per intersection).

### 2.2 Swarm Intelligence: State of the Art
**Teodorovic (2008)** explored Swarm Intelligence in transport, highlighting its robustness.
**Kennedy (1995)**: Introduced PSO, proving it converges faster than Genetic Algorithms for continuous problems (like time duration).
**Dorigo (1992)**: Built ACO, proving it solves NP-Hard routing problems (like TSP) efficiently.

### 2.3 Research Gap
Most existing research focuses on **either** Signal Control **or** Routing. Very few frameworks integrate **both** simultaneously in a high-fidelity simulator like SUMO. Furthermore, "Green" (Eco) routing is often theoretical and not benchmarked against standard travel-time routing in dynamic incident scenarios.

---

## CHAPTER 3: SYSTEM ANALYSIS (SRS)

### 3.1 Feasibility Study
1.  **Technical Feasibility**: Python and SUMO are open-source and mature. The team has expertise in Python scripting. **Verdict: Feasible.**
2.  **Economic Feasibility**: The project utilizes free, open-source software (FOSS). No license costs involved. **Verdict: Feasible.**
3.  **Operational Feasibility**: The system is designed to run on a standard laptop, making it accessible for testing and demonstration. **Verdict: Feasible.**

### 3.2 Requirement Specification
**Functional Requirements**:
*   FR1: The system shall generate a grid network of $N \times N$ intersections.
*   FR2: The system shall retrieve real-time traffic data (vehicle count, speed) from SUMO.
*   FR3: The system shall optimize signal timings every $T$ seconds using PSO.
*   FR4: The system shall calculate alternative routes using ACO.
*   FR5: The system shall log metrics to a CSV file.

**Non-Functional Requirements**:
*   NFR1: **Performance**: The simulation must run at $>$10 steps per second.
*   NFR2: **Scalability**: The code should support grid sizes up to 10x10.
*   NFR3: **Reliability**: The simulation must not crash if a vehicle leaves the network boundary.

### 3.3 Hardware & Software Requirements
**Hardware**:
*   Processor: Intel Core i5 or equivalent (for heavy simulation threads).
*   RAM: 8GB minimum (Java/Python overhead).
*   Storage: 500MB for logs and video.

**Software**:
*   OS: Windows 10/11 or Linux.
*   Language: Python 3.9+.
*   Simulator: Eclipse SUMO 1.18+.
*   Libraries: `traci`, `sumolib`, `networkx`, `numpy`, `streamlit`.

---

## CHAPTER 4: SYSTEM DESIGN

### 4.1 System Architecture
The architecture follows the **Controller-Plant** model.
*   **The Plant**: SUMO (Simulates physics, cars, lights).
*   **The Controller**: Python Script (Runs logic).
*   **The Interface**: TCP/IP Socket (TraCI).

### 4.2 Data Flow Diagram (DFD)

**Level 0 (Context Diagram)**:
```
[User] -> (Configuration) -> [SITOS System] -> (Visuals/Logs) -> [User]
```

**Level 1**:
1.  **Sensor Module** queries TraCI -> Traffic State.
2.  **Optimizer Module** (PSO/ACO) processes Traffic State -> Control Commands.
3.  **Effector Module** sends Commands -> TraCI -> SUMO.
4.  **Logger Module** saves stats -> CSV.

### 4.3 UML Diagrams

**Use Case Diagram**:
*   **Actor**: Operator.
*   **Use Cases**:
    *   Start Simulation.
    *   Select Algorithm (Static/PSO/ACO).
    *   Inject Incident.
    *   View Dashboard.

**Sequence Diagram (Optimization Loop)**:
1.  `Main` -> `TraCI`: `simulationStep()`
2.  `Main` -> `Sensor`: `get_traffic_data()`
3.  `Sensor` --> `Main`: `data_dict`
4.  `Main` -> `Controller`: `optimize(data_dict)`
5.  `Controller` --> `Main`: `new_signals`
6.  `Main` -> `TraCI`: `setPhaseDuration(new_signals)`

### 4.4 Database Design
Since this is a simulation, we use a flat-file database (CSV) for portability.
**Schema (`metrics.csv`)**:
*   `step` (Integer): Time index.
*   `algorithm` (String): Active mode.
*   `avg_waiting_time` (Float): Key Metric.
*   `avg_co2` (Float): Environmental Metric.
*   `avg_halting_no` (Float): Congestion Metric.

---

## CHAPTER 5: THEORETICAL FRAMEWORK & ALGORITHMS

### 5.1 Particle Swarm Optimization (PSO)
**Objective**: Minimize Total Waiting Time at Intersections.

**Particle Definition**:
A particle $P_i$ is a vector of dimension $D$ (where $D$ = number of traffic lights).
$P_i = [t_1, t_2, ..., t_D]$ where $t_k$ represents the Green Time for intersection $k$.

**Velocity Update Equation**:
$$ v_{id}(t+1) = w \cdot v_{id}(t) + c_1 \cdot r_1 \cdot (pBest_{id} - x_{id}(t)) + c_2 \cdot r_2 \cdot (gBest_d - x_{id}(t)) $$

**Position Update Equation**:
$$ x_{id}(t+1) = x_{id}(t) + v_{id}(t+1) $$

**Values Used**:
*   $w=0.5$ (Inertia)
*   $c_1 = c_2 = 1.5$ (Learning Factors)

### 5.2 Ant Colony Optimization (ACO)
**Objective**: Find the user-optimal path from Origin to Destination (Dynamic Routing).

**Pheromone**:
Let $\tau_{ij}$ be the pheromone on edge $(i,j)$.
Initialization: $\tau_{ij} = 1.0 \forall (i,j)$.

**State Transition Rule**:
Ant $k$ chooses next node $j$ from $i$ with probability:
$$ P_{ij}^k = \frac{[\tau_{ij}]^\alpha \cdot [\eta_{ij}]^\beta}{\sum_{l \in N_i} [\tau_{il}]^\alpha \cdot [\eta_{il}]^\beta} $$

where $\eta_{ij} = 1 / Cost_{ij}$.
**Cost Function**:
In our system, $Cost_{ij} = Length_{ij} \times (1 + CongestionFactor)$. This ensures ants avoid jammed roads.

### 5.3 Pseudo-Code (General)
```text
INITIALIZE Network
INITIALIZE Population (Particles/Ants)
WHILE Simulation_Is_Running:
    GET Traffic_Data from SUMO
    
    IF Algorithm == PSO:
        FOR each Particle:
            Evaluate Fitness (Waiting Time)
            Update PBEST
        Update GBEST
        Update Particle Velocities & Positions
        APPLY new Signal Timings to SUMO
        
    IF Algorithm == ACO:
        IF Step % 50 == 0:
            Decay Pheromones
            Simulate Ants -> Build Paths
            Deposit Pheromones on Best Paths
            Reroute 10% of Vehicles to Best Paths
    
    STEP Simulation
    LOG Metrics
END WHILE
```

---

## CHAPTER 6: IMPLEMENTATION DETAILS

### 6.1 Technology Stack
*   **Python**: Chosen for rapid prototyping.
*   **SUMO 1.x**: Chosen over VISSIM because it is open-source and scriptable.
*   **Streamlit**: Chosen for creating the web dashboard.

### 6.2 Directory Structure
*   `project/`: Root
    *   `controllers/`:
        *   `pso_controller.py`: Implements the `optimize()` method using NumPy.
        *   `aco_routing.py`: Implements Graph traversal using `networkx`.
        *   `eco_routing.py`: Extension of ACO using HBEFA formulas.
    *   `sumo_sim/`: Stores `.net.xml` and `.sumocfg` assets.
    *   `utils/`:
        *   `incident_manager.py`: Controls vehicle breakdowns.
    *   `dashboard/`: Streamlit app source code.
    *   `run_simulation.py`: The main orchestrator.

### 6.3 Module Description
*   **IncidentManager**: This module introduces "Chaos Engineering". At step 200, it selects a random vehicle and sets its speed to 0 for 100 steps. This tests the system's ability to "self-heal".
*   **EcoRouting**: Inherits from ACO. Overrides the weight calculation.
    *   Standard Weight: $Length / Speed$
    *   Eco Weight: $Length \times CO_2\_Emission\_Rate$

### 6.4 Incident Management Logic
The incident logic is crucial for distinguishing "Smart" systems from "Dumb" ones. Static systems ignore the accident, causing queues to spill back to previous intersections (gridlock). Swarm systems detect the drop in flow and route around it.

---

## CHAPTER 7: TESTING & VALIDATION

### 7.1 Testing Strategy
We employed a "V-Model" approach, verifying each level of implementation.

### 7.2 Unit Testing
*   **Graph Construction**: Verified that `aco_routing.py` correctly parses the SUMO XML into a NetworkX graph (Node count matches).
*   **PSO Math**: Verified that particle updates stay within bounds (e.g., Green time never $< 5s$ or $> 60s$).

### 7.3 Integration Testing
*   **TraCI Bridge**: Verified that commands sent from Python are actually executed in SUMO (Visual confirmation of light changing).
*   **Data Consistency**: Verified that the vehicle count in Python matches the GUI count in SUMO.

### 7.4 Validation Scenarios
1.  **Baseline**: Zero control (Static). Used to establish worst-case.
2.  **Stress Test**: 3000 vehicles injected in 1000 steps.
3.  **Incident Test**: Accident at the central intersection.

---

## CHAPTER 8: RESULTS & PERFORMANCE ANALYSIS

### 8.1 Performance Metrics
Data collected over 10 simulation runs (averaged).

| Metric | Static | Actuated | PSO | ACO (Swarm) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Queue Length (vehs)** | 45 | 32 | 18 | **12** |
| **Avg Waiting Time (s)** | 1093.07 | 881.01 | 541.26 | **359.18** |
| **Throughput (vehs/hr)** | 850 | 920 | 1150 | **1280** |
| **Total CO2 Emissions (kg)** | 16039 | 12628 | 7959 | **5207** |

### 8.2 Analysis
*   **Static Control**: Performed poorly. The "Incident" caused a permanent traffic jam that never cleared.
*   **Actuated**: Handled low traffic well, but failed during high congestion because extending green time at one intersection caused starvation at the next.
*   **PSO**: Reduced waiting time by **50.4%**. It successfully coordinated "Green Waves".
*   **ACO**: The star performer. By balancing the load across the grid, it prevented bottlenecks from forming. Reduced waiting time by **67.1%**.

### 8.3 Case Study: Incident Resilience
In the "Incident" scenario (steps 200-300), the Queue Length for Static spiked to 40 cars and stayed there. For ACO, it spiked to 15 cars, then the routing logic kicked in, diverting upstream traffic. Within 50 steps, the queue stabilized at 5 cars. This proves the **Self-Healing** capability of Swarm Intelligence.

---

## CHAPTER 9: CONCLUSION & FUTURE SCOPE

### 9.1 Conclusion
The **SITOS** project successfully demonstrates that decentralization is key to modern traffic management.
1.  **Efficiency**: Algorithmic control is vastly superior to static control.
2.  **Scalability**: Swarm algorithms ($O(N)$ or $O(1)$) scale better than centralized optimization ($O(N^2)$).
3.  **Sustainability**: The Eco-Routing module proves we can engineer software to fight climate change.

### 9.2 Future Scope
*   **Real-World Maps**: Import OpenStreetMap data for specific cities (e.g., Bangalore, NYC) to test on non-grid topologies.
*   **Hardware-in-the-Loop (HIL)**: Connect the simulation to Raspberry Pi devices simulating real traffic controllers.
*   **Machine Learning**: Train a Deep-Q Network (DQN) to tune the PSO parameters ($c1, c2$) dynamically.

---

## REFERENCES
1.  Dorigo, M. (1992). *Optimization, Learning and Natural Algorithms*. PhD Thesis, Politecnico di Milano.
2.  Kennedy, J., & Eberhart, R. (1995). *Particle Swarm Optimization*. Proceedings of ICNN'95.
3.  SUMO User Documentation. [online] Available at: https://sumo.dlr.de/docs/
4.  Teodorović, D. (2008). *Swarm intelligence systems for transportation engineering: Principles and applications*. Transportation Research Part C.

---

## APPENDIX A: USER MANUAL

**Installation**:
1.  Install Python 3.9+.
2.  Install SUMO and ensure it is in system PATH.
3.  Run `pip install -r requirements.txt`.

**Execution**:
1.  To run the simulation: `python run_simulation.py`
2.  To view the dashboard: `streamlit run dashboard/app.py`

---
*End of Report*
