import pandas as pd
import numpy as np

class BenchmarkStats:
    def __init__(self):
        self.results = []

    def add_run(self, algorithm, param, metrics_list):
        """
        Add the results of a single simulation run.
        metrics_list: list of dicts {'wait': float, 'co2': float, ...}
        """
        df = pd.DataFrame(metrics_list)
        summary = {
            'Algorithm': algorithm,
            'Param': param,
            'Avg Waiting Time': df['avg_waiting_time'].mean() if 'avg_waiting_time' in df else 0,
            'Avg Queue Length': df['avg_halting_number'].mean() if 'avg_halting_number' in df else 0,
            'Avg CO2': df['avg_co2'].mean() if 'avg_co2' in df else 0,
            'Total Steps': len(df)
        }
        self.results.append(summary)

    def print_summary(self):
        if not self.results:
            print("No benchmark results to show.")
            return

        df = pd.DataFrame(self.results)
        print("\n" + "="*50)
        print("BENCHMARK SUMMARY")
        print("="*50)
        # Reorder columns for readability
        cols = ['Algorithm', 'Param', 'Avg Waiting Time', 'Avg Queue Length', 'Avg CO2']
        # Filter cols that exist
        cols = [c for c in cols if c in df.columns]
        print(df[cols].to_string(index=False))
        print("="*50 + "\n")
        
        # Save to file
        df.to_csv("results/benchmark_summary.csv", index=False)
