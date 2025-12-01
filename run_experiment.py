# run_experiment.py
from dotenv import load_dotenv
import os
import json
import argparse
from utils.result_saver import create_experiment_dir, save_config, save_results_csv, save_summary_csv
from utils.logger import ExperimentLogger
from utils.gantt_plotter import plot_gantt

# Import algorithms
from algorithms.fcfs import run_fcfs
from algorithms.first_fit import run_first_fit
# from algorithms.g_pso import run_g_pso

ALGORITHM_REGISTRY = {
    "fcfs": run_fcfs,
    "first_fit": run_first_fit,
    # "g_pso": run_g_pso,
}

def main():
    parser = argparse.ArgumentParser(description="Run task scheduling experiments.")
    parser.add_argument(
        "--algorithms",
        nargs="+",
        choices=list(ALGORITHM_REGISTRY.keys()),
        default=["fcfs", "first_fit"],
        help="List of algorithms to run (e.g., --algorithms fcfs first_fit)"
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
        results = algo_func(tasks, vm_names, logger)

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