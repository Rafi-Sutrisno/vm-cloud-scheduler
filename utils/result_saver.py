# utils/result_saver.py
import os
import json
import csv
from datetime import datetime

def create_experiment_dir():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    exp_dir = f"results/experiment_{timestamp}"
    os.makedirs(exp_dir, exist_ok=True)
    return exp_dir

def save_config(exp_dir, vm_config, task_params):
    with open(f"{exp_dir}/config.json", "w") as f:
        json.dump({
            "vm_config": vm_config,
            "task_distribution": task_params,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)

def save_results_csv(exp_dir, schedule_results, algo_name):
    filepath = f"{exp_dir}/{algo_name}_results.csv"
    fieldnames = ["task_id", "duration", "vm", "start", "end"]
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in schedule_results:
            # Keep only the needed keys
            filtered_row = {k: row[k] for k in fieldnames if k in row}
            writer.writerow(filtered_row)

def save_summary_csv(exp_dir, summary):
    with open(f"{exp_dir}/makespan_summary.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Makespan (s)"])
        for algo, ms in summary.items():
            writer.writerow([algo, f"{ms:.2f}"])