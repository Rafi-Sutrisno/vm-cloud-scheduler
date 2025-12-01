# utils/gantt_plotter.py
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_gantt(schedule_results, exp_dir, vm_names, algo_name):
    fig, ax = plt.subplots(figsize=(12, 6))
    vm_tasks = defaultdict(list)
    for r in schedule_results:
        vm_tasks[r["vm"]].append((r["start"], r["end"], r["task_id"]))

    colors = plt.cm.tab10(range(len(vm_names)))
    for i, vm in enumerate(vm_names):
        for start, end, tid in vm_tasks[vm]:
            ax.barh(vm, end - start, left=start, color=colors[i], edgecolor='black', alpha=0.7)
            ax.text(start + (end - start)/2, i, f"T{tid}", color="white", ha="center", va="center")

    ax.set_xlabel("Time (seconds)")
    ax.set_title("Gantt Chart of Task Execution per VM for {algo}".format(algo=algo_name))
    plt.tight_layout()
    plt.savefig(f"{exp_dir}/gantt_chart_{algo_name}.png")
    # plt.show()