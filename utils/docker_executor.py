# utils/docker_executor.py
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

def run_single_task_in_vm(vm: str, duration: float, task_id: int, logger=None) -> Dict:
    """
    Execute ONE task inside a VM container.
    Returns dict with timing and metadata.
    """
    scaled_duration = duration
    start = time.time()
    result = subprocess.run(
        ["docker", "exec", vm, "python3", "/task_runner.py", str(scaled_duration)],
        capture_output=True, text=True
    )
    end = time.time()

    event = {
        "task_id": task_id,
        "vm": vm,
        "duration": duration,
        "start": start,
        "end": end,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip()
    }

    msg = f"[{vm}] Task {task_id} ({duration:.2f} MI) completed in {end - start:.3f}s"
    if logger:
        logger.log(msg)
    else:
        print(msg)

    return event

def run_tasks_parallel(assignments: List[tuple], logger=None) -> List[Dict]:
    """
    Run multiple tasks in parallel.
    assignments = [(task_id, vm, duration), ...]
    """
    results = []
    # Use one thread per VM to avoid overwhelming Docker
    with ThreadPoolExecutor(max_workers=len(set(vm for _, vm, _ in assignments))) as executor:
        futures = [
            executor.submit(run_single_task_in_vm, vm, duration, tid, logger)
            for (tid, vm, duration) in assignments
        ]
        for future in as_completed(futures):
            results.append(future.result())
    return results