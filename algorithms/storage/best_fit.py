from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

# VM MIPS (just for reference)
VM_MIPS = {
    "vm1": 1000,
    "vm2": 1000,
    "vm3": 1000,
    "vm4": 1000,
    "vm5": 1000,
}

def run_best_fit(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    # Initialize VM loads to zero
    vm_load = {vm: 0.0 for vm in vm_names}  # estimated time per VM

    assignments = []

    # For each task, choose the VM with the best fit (least current load)
    for i, task_mi in enumerate(tasks):
        candidates = []
        
        # Compute the task execution time for each VM and track the current load
        for vm in vm_names:
            exec_time = task_mi / VM_MIPS[vm]
            candidates.append((vm_load[vm], vm))  # Sort based on current load
        
        # Sort VMs by their current load (smallest load first)
        candidates.sort(key=lambda x: x[0])

        # Select the VM with the least current load
        best_vm = candidates[0][1]
        
        # Calculate the execution time and update the VM load
        exec_time = task_mi / VM_MIPS[best_vm]
        vm_load[best_vm] += exec_time

        # Log or print assignment details
        msg = f"[Best-Fit] Task {i} ({task_mi} MI) → {best_vm} | load: {vm_load[best_vm]:.3f}s"
        if logger:
            logger.log(msg)
        else:
            print(msg)

        assignments.append((i, best_vm, task_mi))

    return run_tasks_parallel(assignments, logger)

run_best_fit = run_best_fit
