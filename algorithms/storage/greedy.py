from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

# VM performance in MIPS (from .env OR override here)
VM_MIPS = {
    "vm1": 1000,
    "vm2": 1000,
    "vm3": 1000,
    "vm4": 1000,
    "vm5": 1000,
}

def run_greedy(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    vm_load = {vm: 0.0 for vm in vm_names}       # estimated time
    vm_task_count = {vm: 0 for vm in vm_names}   # tie-breaking

    assignments = []

    for i, task_mi in enumerate(tasks):
        # Compute predicted finish time on each VM
        candidates = []
        for vm in vm_names:
            exec_time = task_mi / VM_MIPS[vm]
            finish = vm_load[vm] + exec_time
            candidates.append((finish, vm_task_count[vm], vm))

        candidates.sort(key=lambda x: (x[0], x[1]))
        target_vm = candidates[0][2]

        exec_time = task_mi / VM_MIPS[target_vm]
        vm_load[target_vm] += exec_time
        vm_task_count[target_vm] += 1

        msg = f"[Greedy] Task {i} ({task_mi} MI) → {target_vm} | predicted load: {vm_load[target_vm]:.3f}s"
        (logger.log(msg) if logger else print(msg))

        assignments.append((i, target_vm, task_mi))

    return run_tasks_parallel(assignments, logger)

run_greedy = run_greedy
