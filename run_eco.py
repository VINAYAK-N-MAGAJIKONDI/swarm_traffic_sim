from run_simulation import start_simulation, cleanup

if __name__ == "__main__":
    # cleanup() # Optional: keeps old data if commented out, so we can compare Eco vs others if they exist
    print("Running Eco Routing Simulation...")
    # Run Eco with 10 Ants
    start_simulation(algorithm="Eco", param=10)
