# algorithms/priority.py
from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

VM_MIPS = {
    "vm1": 5000,
    "vm2": 6000,
    "vm3": 7000,
    "vm4": 8000,
    "vm5": 10000,
}

# You'll receive VM_MIPS from run_experiment.py (see Step 3)
def run_priority(tasks: List[Dict], vm_names: List[str], logger=None) -> List[Dict]:
    # Step 1: Compute priority for each task
    indexed_tasks = []
    for i, task in enumerate(tasks):
        mi = task["mi"]
        sla = task["sla"]
        # Priority score: lower = more urgent
        priority_score = mi / sla  # or sla alone, or (mi * (1/sla))
        indexed_tasks.append((i, task, priority_score))
    
    # Step 2: Sort by priority (ascending = most urgent first)
    indexed_tasks.sort(key=lambda x: x[2])  # lowest score first = highest priority

    # Step 3: Assign using least-loaded VM (like your FCFS)
    vm_load = {vm: 0.0 for vm in vm_names}
    assignments = []

    for i, task, _ in indexed_tasks:
        task_id = i
        task_mi = task["mi"]
        # Find least-loaded VM (in estimated time)
        best_vm = min(vm_names, key=lambda vm: vm_load[vm])
        exec_time = task_mi / VM_MIPS[best_vm]
        vm_load[best_vm] += exec_time

        msg = f"[PRIORITY] Task {task_id} ({task_mi} MI, SLA={task['sla']}) → {best_vm} | load: {vm_load[best_vm]:.3f}s"
        if logger:
            logger.log(msg)
        else:
            print(msg)

        assignments.append((task_id, best_vm, task_mi))

    return run_tasks_parallel(assignments, logger)