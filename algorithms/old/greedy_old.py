# algorithms/greedy.py
from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

# PRE-COMPUTE VM_MIPS from .env (or pass it in)
VM_MIPS = {
    "vm1": 1000,
    "vm2": 1000,
    "vm3": 1000,
    "vm4": 1000,
    "vm5": 1000,
}

def run_greedy(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    # Track current load (simulated execution time) per VM
    vm_load = {vm: 0.0 for vm in vm_names}
    # Track number of tasks per VM (for tie-breaking)
    vm_task_count = {vm: 0 for vm in vm_names}

    assignments = []

    for i, task_mi in enumerate(tasks):
        # Calculate expected finish time for each VM
        candidates = []
        for vm in vm_names:
            exec_time = task_mi / VM_MIPS[vm]
            finish_time = vm_load[vm] + exec_time
            candidates.append((finish_time, vm_task_count[vm], vm))

        # Sort by finish time (ascending), then by task count (ascending)
        candidates.sort(key=lambda x: (x[0], x[1]))
        target_vm = candidates[0][2]

        # Update load and task count
        exec_time = task_mi / VM_MIPS[target_vm]
        vm_load[target_vm] += exec_time
        vm_task_count[target_vm] += 1

        msg = f"GreedyLoadBalancer: Task {i} ({task_mi} MI) → {target_vm} (load: {vm_load[target_vm]:.2f}s)"
        if logger: logger.log(msg)
        else: print(msg)

        assignments.append((i, target_vm, task_mi))

    # Run all in parallel
    results = run_tasks_parallel(assignments, logger)
    return results

run_greedy = run_greedy