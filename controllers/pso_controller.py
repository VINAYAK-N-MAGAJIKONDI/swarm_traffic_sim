import numpy as np

# PSO-based signal control logic
# Implement your Particle Swarm Optimization controller here

class PSOController:
    def __init__(self,
                 num_particles=50,
                 num_iterations=60,
                 cycle_length=120,
                 min_green=5,
                 max_green=60):
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.cycle_length = cycle_length
        self.min_green = min_green
        self.max_green = max_green

    def normalize_cycle(self, timings):
        timings = np.clip(timings, self.min_green, self.max_green)
        total = np.sum(timings)
        if total == 0: return np.full_like(timings, self.cycle_length / len(timings))
        return (timings / total) * self.cycle_length

    def fitness(self, timings, simulate_function):
        results = simulate_function(timings)

        delay = results.get("total_delay", 0)
        queue = results.get("total_queue", 0)
        teleports = results.get("teleports", 0)
        throughput = results.get("throughput", 0)
        spillback = results.get("spillback", 0)

        # IEEE Advanced: Zero-tolerance for teleports
        if teleports > 0:
            return 1e12

        # IEEE Standard Multi-objective Fitness
        score = (
            0.4 * delay +
            0.3 * queue +
            0.2 * spillback * 1000 -
            0.3 * throughput
        )
        return score

    def optimize(self, simulate_function, dimension):
        if dimension == 0: return []

        particles = np.random.uniform(self.min_green, self.max_green, (self.num_particles, dimension))
        particles = np.array([self.normalize_cycle(p) for p in particles])

        velocities = np.zeros_like(particles)

        personal_best = particles.copy()
        personal_scores = np.full(self.num_particles, np.inf)

        global_best = None
        global_score = np.inf

        w_max, w_min = 0.9, 0.4
        c1, c2 = 2.0, 2.0

        for iteration in range(self.num_iterations):
            w = w_max - (w_max - w_min) * (iteration / self.num_iterations)

            for i in range(self.num_particles):
                score = self.fitness(particles[i], simulate_function)

                if score < personal_scores[i]:
                    personal_best[i] = particles[i]
                    personal_scores[i] = score

                if score < global_score:
                    global_best = particles[i].copy()
                    global_score = score

            for i in range(self.num_particles):
                r1, r2 = np.random.rand(), np.random.rand()

                velocities[i] = (
                    w * velocities[i] +
                    c1 * r1 * (personal_best[i] - particles[i]) +
                    c2 * r2 * (global_best - particles[i])
                )

                particles[i] += velocities[i]
                particles[i] = self.normalize_cycle(particles[i])

        return global_best

    def optimize_signal_timing(self, traffic_data):
        edge_ids = [k for k in traffic_data.keys() if k != '__network__']
        dim = len(edge_ids)
        
        def predictive_proxy(timings):
            p_delay = 0
            p_queue = 0
            p_spillback = 0
            
            for i, tid in enumerate(edge_ids):
                data = traffic_data.get(tid, {})
                w = data.get('waiting_time', 0)
                h = data.get('halting_number', 0)
                l = data.get('length', 100)
                g = timings[i]
                
                # Heuristic: Delay/Queue scaled by (Cycle/Green)
                # If green is low, vehicles accumulate more waiting time
                fact = (self.cycle_length / max(g, 1.0))
                p_delay += w * fact
                p_queue += h * fact
                
                # Spillback heuristic: queue is > 80% of edge length
                # Each vehicle takes ~7.5m (sumo default)
                if h * 7.5 > l * 0.8:
                    p_spillback += 1
            
            return {
                "total_delay": p_delay,
                "total_queue": p_queue,
                "teleports": traffic_data.get('__network__', {}).get('teleports', 0),
                "spillback": p_spillback,
                "throughput": traffic_data.get('__network__', {}).get('throughput', 0)
            }

        return self.optimize(predictive_proxy, dim)



