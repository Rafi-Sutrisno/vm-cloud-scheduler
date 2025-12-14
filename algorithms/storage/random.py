from typing import List, Dict
from utils.docker_executor import run_tasks_parallel
import random

def run_random(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    assignments = []

    for i, task_mi in enumerate(tasks):
        # Randomly choose a VM
        vm = random.choice(vm_names)

        msg = f"[Random] Task {i} ({task_mi} MI) → {vm}"
        if logger:
            logger.log(msg)
        else:
            print(msg)

        assignments.append((i, vm, task_mi))

    return run_tasks_parallel(assignments, logger)

run_random = run_random
