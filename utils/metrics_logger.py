import csv

def log_metrics(metrics, filename='results/logs/metrics.csv'):
    """Append metrics to a CSV file."""
    fieldnames = list(metrics.keys())
    file_exists = False
    try:
        with open(filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(metrics)
