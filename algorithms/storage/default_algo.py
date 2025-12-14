# algorithms/default_algo.py
from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

def run_default(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    if logger:
        logger.log("[Default Scheduler (Round-Robin Assignment)]")
    else:
        print("[Default Scheduler (Round-Robin Assignment)]")

    # Build assignment list BEFORE execution
    assignments = []
    for i, task in enumerate(tasks):
        vm = vm_names[i % len(vm_names)]
        assignments.append((i, vm, task))
        msg = f"Task {i:2d} ({task:4.2f} MI) → {vm}"
        if logger:
            logger.log(msg)
        else:
            print(msg)

    # Run all in parallel
    results = run_tasks_parallel(assignments, logger)
    return results

run_default = run_default