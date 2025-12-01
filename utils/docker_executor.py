# utils/docker_executor.py
import subprocess
import time

def run_task_in_vm(vm: str, duration: float) -> tuple:
    start = time.time()
    result = subprocess.run(
        ["docker", "exec", vm, "python3", "/task_runner.py", str(duration)],
        capture_output=True, text=True
    )
    end = time.time()
    print(f"[{vm}] {result.stdout.strip()}")
    if result.stderr: print(f"[{vm} ERROR] {result.stderr.strip()}")
    return start, end