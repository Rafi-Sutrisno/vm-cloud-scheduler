# utils/docker_stats_plotter.py
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_docker_stats(exp_dir: str, algo_name: str):
    csv_path = os.path.join(exp_dir, f"docker_stats_{algo_name}.csv")
    if not os.path.exists(csv_path):
        print(f"[WARN] No stats file for {algo_name}")
        return

    # Load data
    df = pd.read_csv(csv_path)
    df['relative_time'] = df['timestamp'] - df['timestamp'].min()

    # Group by container
    vm_groups = df.groupby('container')

    plt.figure(figsize=(12, 6))
    for vm, group in vm_groups:
        plt.plot(group['relative_time'], group['cpu_percent'].astype(float), label=vm, marker='o', markersize=3)

    plt.title(f"CPU Usage Over Time — {algo_name.upper()}")
    plt.xlabel("Time (seconds since start)")
    plt.ylabel("CPU %")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plot_path = os.path.join(exp_dir, f"docker_cpu_{algo_name}.png")
    plt.savefig(plot_path)
    plt.close()  # Prevent display in headless mode
    print(f"✅ CPU plot saved: {plot_path}")