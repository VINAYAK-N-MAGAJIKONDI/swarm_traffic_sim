import numpy as np

# PSO-based signal control logic
# Implement your Particle Swarm Optimization controller here

class PSOController:
    def __init__(self, num_particles=10, num_iterations=20):
        self.num_particles = num_particles
        self.num_iterations = num_iterations

    def optimize(self, traffic_data):
        # Example: optimize signal timings for intersections
        num_signals = len(traffic_data)
        particles = np.random.uniform(10, 60, (self.num_particles, num_signals))  # signal timings
        velocities = np.zeros_like(particles)
        personal_best = particles.copy()
        personal_best_scores = np.array([self.fitness(p, traffic_data) for p in particles])
        global_best = personal_best[np.argmin(personal_best_scores)]
        global_best_score = np.min(personal_best_scores)
        w, c1, c2 = 0.5, 1.5, 1.5
        for _ in range(self.num_iterations):
            for i in range(self.num_particles):
                r1, r2 = np.random.rand(), np.random.rand()
                velocities[i] = w * velocities[i] + c1 * r1 * (personal_best[i] - particles[i]) + c2 * r2 * (global_best - particles[i])
                particles[i] += velocities[i]
                score = self.fitness(particles[i], traffic_data)
                if score < personal_best_scores[i]:
                    personal_best[i] = particles[i]
                    personal_best_scores[i] = score
            best_idx = np.argmin(personal_best_scores)
            if personal_best_scores[best_idx] < global_best_score:
                global_best = personal_best[best_idx]
                global_best_score = personal_best_scores[best_idx]
        return global_best

    def fitness(self, timings, traffic_data):
        # Dummy fitness: sum of timings (replace with real wait time calculation)
        return np.sum(timings)

    def optimize_signal_timing(self, traffic_data):
        return self.optimize(traffic_data)
