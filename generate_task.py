# generate_tasks.py
import random
import json
import matplotlib.pyplot as plt

def generate_tasks(n=50):
    tasks = []
    num_high = int(0.3 * n)
    num_medium = int(0.3 * n)
    num_small = n - num_high - num_medium 

    # High: 4–6s
    tasks += [round(random.uniform(4.0, 6.0), 2) for _ in range(num_high)]
    # Medium: 2–4s
    tasks += [round(random.uniform(2.0, 4.0), 2) for _ in range(num_medium)]
    # Small: 0.5–2s
    tasks += [round(random.uniform(0.5, 2.0), 2) for _ in range(num_small)]

    # Shuffle to avoid bias
    random.shuffle(tasks)
    return tasks

def plot_tasks(tasks, save_path="./storage/task/task_distribution.png"):
    plt.figure(figsize=(10, 5))
    plt.hist(tasks, bins=20, color='skyblue', edgecolor='black')
    plt.title("Task Duration Distribution (seconds)")
    plt.xlabel("Task Duration (s)")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(save_path)
    plt.show()
    print(f"✅ Task distribution saved to {save_path}")

if __name__ == "__main__":
    TASKS = generate_tasks(50)
    with open("./storage/task/tasks.json", "w") as f:
        json.dump(TASKS, f)
    print(f"Generated {len(TASKS)} tasks.")
    print("Sample tasks:", TASKS[:10])
    plot_tasks(TASKS)