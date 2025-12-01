# task_runner.py
import time
import sys

if len(sys.argv) != 2:
    print("Usage: python task_runner.py <seconds>")
    sys.exit(1)

duration = float(sys.argv[1])
print(f"[Task] Simulating CPU-bound work for {duration} seconds...")
start = time.time()
while time.time() - start < duration:
    pass  
print(f"[Task] Completed after {time.time() - start:.2f} seconds.")