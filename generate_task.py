import random
import json
import matplotlib.pyplot as plt

def generate_tasks(n=50):
    tasks = []
    num_high = int(0.3 * n)
    num_medium = int(0.3 * n)
    num_small = n - num_high - num_medium 

    # High MI: 800–1200 MI
    tasks += [round(random.uniform(800, 1200), 1) for _ in range(num_high)]
    # Medium MI: 300–600 MI
    tasks += [round(random.uniform(300, 600), 1) for _ in range(num_medium)]
    # Small MI: 50–200 MI
    tasks += [round(random.uniform(50, 200), 1) for _ in range(num_small)]

    random.shuffle(tasks)
    return tasks

def plot_tasks(tasks, save_path="./storage/task/task_distribution.png"):
    plt.figure(figsize=(10, 5))
    plt.hist(tasks, bins=20, color='skyblue', edgecolor='black')
    plt.title("Task Workload Distribution (Millions of Instructions)")
    plt.xlabel("Task Size (MI)")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(save_path)
    plt.show()
    print(f"✅ Task distribution saved to {save_path}")

if __name__ == "__main__":
    TASKS = generate_tasks(50)
    with open("./storage/task/tasks.json", "w") as f:
        json.dump(TASKS, f)
    print(f"Generated {len(TASKS)} MI-based tasks.")
    print("Sample tasks:", TASKS[:10])
    plot_tasks(TASKS)
