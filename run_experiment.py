# run_experiment.py
from dotenv import load_dotenv
import os
import json
import argparse
from utils.result_saver import create_experiment_dir, save_config, save_results_csv, save_summary_csv
from utils.logger import ExperimentLogger
from utils.gantt_plotter import plot_gantt

# Import algorithms
from algorithms.default_algo import run_default
# from algorithms.first_fit import run_first_fit
# from algorithms.g_pso import run_g_pso
# from algorithms.g_pso_2 import run_g_pso_2
from algorithms.greedy import run_greedy

from utils.docker_stats_logger import DockerStatsLogger
from utils.docker_stats_plotter import plot_docker_stats
import threading
import time

def log_docker_stats_periodically(stats_logger, stop_event, interval=0.5):
    while not stop_event.is_set():
        stats_logger.log_stats()
        time.sleep(interval)

ALGORITHM_REGISTRY = {
    "default": run_default,
    "greedy": run_greedy,
}

def main():
    parser = argparse.ArgumentParser(description="Run task scheduling experiments.")
    parser.add_argument(
        "--algorithms",
        nargs="+",
        choices=list(ALGORITHM_REGISTRY.keys()),
        default=[ "default", "greedy"],
        help="List of algorithms to run (e.g., --algorithms default greedy)"
    )
    parser.add_argument(
        "--tasks",
        type=str,
        default="./storage/task/tasks.json",
        help="Path to tasks JSON file"
    )
    args = parser.parse_args()

    load_dotenv()
    
    exp_dir = create_experiment_dir()
    logger = ExperimentLogger(exp_dir)

    # Load tasks
    with open(args.tasks, "r") as f:
        tasks = json.load(f)

    # Load VM config from .env
    vm_config = {f"vm{i+1}": float(os.getenv(f"VM{i+1}_CPUS")) for i in range(5)}
    vm_names = list(vm_config.keys())

    VM_MIPS = {}
    for i, vm in enumerate(vm_names):
        cpu_quota = float(os.getenv(f"VM{i+1}_CPUS"))
        # Linear map: 0.5 → 500, 0.6 → 600, ..., 1.0 → 1000
        mips = int(500 + (cpu_quota - 0.5) * (1000 - 500) / (1.0 - 0.5))
        VM_MIPS[vm] = mips

    # Ensure task_runner.py is in all containers (one-time setup)
    import subprocess
    for vm in vm_names:
        subprocess.run(["docker", "cp", "task_runner.py", f"{vm}:/task_runner.py"], check=True)

    save_config(exp_dir, vm_config, {
        "num_tasks": len(tasks),
        "algorithms_run": args.algorithms,
        "task_file": args.tasks
    })

    logger.log(f"🚀 Running experiments with algorithms: {', '.join(args.algorithms)}")
    logger.log(f"Loading {len(tasks)} tasks from {args.tasks}")

    # Run selected algorithms
    summary = {}
    all_results = {}

    for algo_name in args.algorithms:
        algo_func = ALGORITHM_REGISTRY[algo_name]
        logger.log(f"\n▶️  Running {algo_name.upper()}...")

        # Start Docker stats logging
        stats_logger = DockerStatsLogger(exp_dir, vm_names, algo_name)
        stop_stats = threading.Event()
        stats_thread = threading.Thread(
            target=log_docker_stats_periodically,
            args=(stats_logger, stop_stats)
        )
        stats_thread.start()

        results = algo_func(tasks, vm_names, logger)

        # Stop stats logging
        stop_stats.set()
        stats_thread.join()

        plot_docker_stats(exp_dir, algo_name)

        start_times = [r["start"] for r in results]
        end_times = [r["end"] for r in results]
        makespan = max(end_times) - min(start_times)

        summary[algo_name] = makespan
        all_results[algo_name] = results

        save_results_csv(exp_dir, results, algo_name)

        plot_gantt(results, exp_dir, vm_names, algo_name)

    # Save summary
    save_summary_csv(exp_dir, summary)

    # Plot Gantt for best-performing algorithm
    if len(all_results) > 0:
        best_algo = min(summary, key=summary.get)
        logger.log(f"🏆 Best algorithm: {best_algo.upper()} (makespan: {summary[best_algo]:.2f}s)")
        # plot_gantt(all_results[best_algo], exp_dir, vm_names, best_algo)

    logger.log(f"✅ Experiment complete! Results saved to: {exp_dir}")

if __name__ == "__main__":
    main()