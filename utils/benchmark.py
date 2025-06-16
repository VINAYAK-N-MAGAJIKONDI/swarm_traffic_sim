import time
import tracemalloc

def benchmark_algorithm(algorithm_func, *args, **kwargs):
    tracemalloc.start()
    start_time = time.time()
    result = algorithm_func(*args, **kwargs)
    elapsed_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        'result': result,
        'elapsed_time': elapsed_time,
        'memory_usage': peak / 1024  # in KB
    }

def write_benchmark_report(report, filename='results/benchmark_report.md'):
    with open(filename, 'w') as f:
        f.write('# Benchmark Report\n')
        for algo, data in report.items():
            f.write(f'## {algo}\n')
            f.write(f"Time: {data['elapsed_time']:.4f} s\n")
            f.write(f"Memory: {data['memory_usage']:.2f} KB\n\n")
