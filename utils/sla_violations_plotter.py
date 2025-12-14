import matplotlib.pyplot as plt
from typing import List, Dict

def plot_sla_violations(tasks: List[Dict], results: List[Dict], save_path: str, algo_name: str):
    sla_violations = []
    
    global_start_time = results[0]["start"]

    for task, result in zip(tasks, results):
        sla_deadline = task["sla"]  # SLA deadline in seconds (relative to start time)
        start_time = global_start_time
        end_time = result["end"]  # End time of the task (Unix timestamp)
        
        # Calculate the actual SLA deadline (start time + SLA)
        actual_sla_deadline = start_time + sla_deadline
        
        # Check for SLA violation: if end_time is greater than the SLA deadline, it's a violation
        violation = end_time > actual_sla_deadline
        sla_violations.append(violation)

    # Calculate the violation count and the percentage of violations
    violation_count = sum(sla_violations)
    total_tasks = len(sla_violations)
    violation_percentage = (violation_count / total_tasks) * 100

    # Visualize the number of violations
    plt.figure(figsize=(8, 6))
    plt.bar(["Violations", "Compliant"], [violation_count, total_tasks - violation_count], color=['red', 'green'])
    plt.title(f"SLA Violation Summary for {algo_name.upper()}\nTotal Tasks: {total_tasks} | Violations: {violation_count} ({violation_percentage:.2f}%)")
    plt.xlabel("Violation Status")
    plt.ylabel("Task Count")
    plt.tight_layout()

    # Save the plot to the specified directory
    plt.savefig(f"{save_path}/sla_plot_{algo_name}.png")

    print(f"✅ SLA violation chart saved to {save_path}/sla_plot_{algo_name}.png")
