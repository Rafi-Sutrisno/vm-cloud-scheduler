# task_runner.py
import sys
import time

if len(sys.argv) != 2:
    print("Usage: python task_runner.py <task_mi>")
    sys.exit(1)

try:
    task_mi = float(sys.argv[1])
except ValueError:
    print("Error: task_mi must be a number (e.g., 1000 for 1000 MI)")
    sys.exit(1)

# Scale MI to loop iterations (e.g., 1 MI = 1000 integer ops)
# Adjust SCALE_FACTOR to control real runtime (start with 1000)
SCALE_FACTOR = 1000
iterations = int(task_mi * SCALE_FACTOR)

print(f"[Task] Executing {task_mi:.1f} MI ({iterations:,} iterations)...")

start = time.time()

# CPU-bound computation: integer multiply + add (no I/O, no sleep)
total = 0
for i in range(iterations):
    total += i * i  # This is real work

end = time.time()

print(f"[Task] Completed {task_mi:.1f} MI in {end - start:.2f} seconds.")