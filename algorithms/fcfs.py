# algorithms/fcfs.py
from typing import List, Dict
from utils.docker_executor import run_task_in_vm

def fcfs_scheduler(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    if logger:
        logger.log("[FCFS Scheduler (Round-Robin Assignment)]")
    else:
        print("[FCFS Scheduler (Round-Robin Assignment)]")

    task_events = []
    for i, task in enumerate(tasks):
        vm = vm_names[i % len(vm_names)]
        msg = f"Task {i:2d} ({task:4.2f}s) → {vm}"
        if logger:
            logger.log(msg)
        else:
            print(msg)
        start, end = run_task_in_vm(vm, task)
        task_events.append({
            "task_id": i,
            "duration": task,
            "vm": vm,
            "start": start,
            "end": end
        })
    return task_events

run_fcfs = fcfs_scheduler