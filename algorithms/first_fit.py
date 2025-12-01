# algorithms/first_fit.py
from typing import List, Dict
from utils.docker_executor import run_task_in_vm  

def run_first_fit(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    vm_load = {vm: 0.0 for vm in vm_names}
    events = []
    for i, task in enumerate(tasks):
        vm = min(vm_names, key=lambda v: vm_load[v])
        vm_load[vm] += task
        msg = f"FirstFit: Task {i} ({task:.2f}s) → {vm} (load: {vm_load[vm]:.2f}s)"
        if logger: logger.log(msg)
        else: print(msg)
        start, end = run_task_in_vm(vm, task)
        events.append({"task_id": i, "duration": task, "vm": vm, "start": start, "end": end})
    return events