# algorithms/first_fit.py
from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

# PRE-COMPUTE VM_MIPS from .env (or pass it in)
VM_MIPS = {
    "vm1": 500,
    "vm2": 800,
    "vm3": 1000,
    "vm4": 600,
    "vm5": 900,
}

def run_first_fit(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    # vm_load now tracks SIMULATED EXECUTION TIME (seconds), not raw task sum
    vm_load = {vm: 0.0 for vm in vm_names}
    assignments = []

    for i, task_mi in enumerate(tasks):
        # Find VM with smallest LOAD = Σ(MI / MIPS)
        target_vm = min(vm_names, key=lambda v: vm_load[v])
        exec_time = task_mi / VM_MIPS[target_vm]
        vm_load[target_vm] += exec_time

        msg = f"FirstFit: Task {i} ({task_mi} MI) → {target_vm} (load: {vm_load[target_vm]:.2f}s)"
        if logger: logger.log(msg)
        else: print(msg)

        assignments.append((i, target_vm, task_mi))

    # Then run tasks in parallel...
    results = run_tasks_parallel(assignments, logger)
    return results