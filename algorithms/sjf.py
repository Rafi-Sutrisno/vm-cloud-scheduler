from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

VM_MIPS = {
    "vm1": 5000,
    "vm2": 6000,
    "vm3": 7000,
    "vm4": 8000,
    "vm5": 10000,
}

def run_sjf(tasks: List[Dict], vm_names: List[str], logger=None) -> List[Dict]:
    # Sort tasks by ascending MI (Shortest Task First)
    tasks_sorted = sorted(enumerate(tasks), key=lambda x: x[1]["mi"])

    vm_load = {vm: 0.0 for vm in vm_names}  # estimated time per VM

    assignments = []

    for i, task in tasks_sorted:
        task_mi = task["mi"]
        # Find the VM with the least load (minimizing waiting time for tasks)
        best_vm = min(vm_names, key=lambda vm: vm_load[vm])
        exec_time = task_mi / VM_MIPS[best_vm]
        vm_load[best_vm] += exec_time

        msg = f"[STF] Task {i} ({task_mi} MI) → {best_vm} | load: {vm_load[best_vm]:.3f}s"
        if logger:
            logger.log(msg)
        else:
            print(msg)

        assignments.append((i, best_vm, task_mi))

    return run_tasks_parallel(assignments, logger)

run_sjf = run_sjf
