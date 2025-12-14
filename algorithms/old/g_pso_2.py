# algorithms/g_pso.py
import random
import math
from typing import List, Dict
from utils.docker_executor import run_tasks_parallel

# PRE-COMPUTE VM_MIPS from .env (or pass it in)
VM_MIPS = {
    "vm1": 500,
    "vm2": 800,
    "vm3": 1000,
    "vm4": 600,
    "vm5": 900,
}

def compute_makespan(schedule: List[int], tasks_mi: List[float], vm_mips_list: List[float]) -> float:
    """Given a schedule (list of VM indices for each task),
    compute total makespan = max(load per VM)
    """
    vm_load = [0.0 for _ in vm_mips_list]
    for task_id, vm_idx in enumerate(schedule):
        exec_time = tasks_mi[task_id] / vm_mips_list[vm_idx]
        vm_load[vm_idx] += exec_time
    return max(vm_load)

def compute_load_balance(schedule: List[int], tasks_mi: List[float], vm_mips_list: List[float]) -> float:
    """LoadLevel = min_load / max_load"""
    vm_load = [0.0 for _ in vm_mips_list]
    for task_id, vm_idx in enumerate(schedule):
        exec_time = tasks_mi[task_id] / vm_mips_list[vm_idx]
        vm_load[vm_idx] += exec_time
    min_load = min(vm_load)
    max_load = max(vm_load)
    return min_load / max_load if max_load > 0 else 0.0

def greedy_initialization(tasks_mi: List[float], vm_mips_list: List[float]) -> List[int]:
    """
    Greedy procedure (from paper Section 3.6):
    - For each task, assign to VM that gives minimal current makespan.
    - Tie-break: assign to VM with fewer tasks.
    """
    schedule = []
    vm_load = [0.0 for _ in vm_mips_list]
    vm_task_count = [0 for _ in vm_mips_list]

    for task_id, mi in enumerate(tasks_mi):
        best_vm = 0
        best_makespan = float('inf')
        for vm_idx, mips in enumerate(vm_mips_list):
            new_load = vm_load[vm_idx] + estimate_task_time(mi, mips)
            # Temporarily compute makespan if assigned to this VM
            temp_loads = vm_load.copy()
            temp_loads[vm_idx] = new_load
            temp_makespan = max(temp_loads)
            if (temp_makespan < best_makespan or
                (math.isclose(temp_makespan, best_makespan) and vm_task_count[vm_idx] < vm_task_count[best_vm])):
                best_makespan = temp_makespan
                best_vm = vm_idx
        schedule.append(best_vm)
        vm_load[best_vm] += estimate_task_time(mi, vm_mips_list[best_vm])
        vm_task_count[best_vm] += 1
    return schedule

def estimate_task_time(task_mi: float, vm_mips: float) -> float:
    return task_mi / vm_mips

def run_g_pso(tasks: List[float], vm_names: List[str], logger=None) -> List[Dict]:
    if logger:
        logger.log("[G&PSO Scheduler (Greedy + PSO)]")
    else:
        print("[G&PSO Scheduler (Greedy + PSO)]")

    # === Map VM names to MIPS indices ===
    vm_mips = [VM_MIPS[vm] for vm in vm_names]

    # === PSO Parameters (from paper Table 1) ===
    num_particles = 100
    max_iter = 200
    inertia_weight = 0.9
    c1 = c2 = 2.0
    num_vms = len(vm_names)
    num_tasks = len(tasks)

    # === Initialize Particles ===
    particles = []
    velocities = []
    pbest = []      # personal best positions
    pbest_fit = []  # personal best fitness

    for _ in range(num_particles):
        # Random initial schedule: each task assigned to random VM (0 to num_vms-1)
        pos = [random.randint(0, num_vms - 1) for _ in range(num_tasks)]
        vel = [random.uniform(-(num_vms - 1), num_vms - 1) for _ in range(num_tasks)]
        particles.append(pos)
        velocities.append(vel)
        pbest.append(pos.copy())
        fit = 1.0 / compute_makespan(pos, tasks, vm_mips)
        pbest_fit.append(fit)

    # === Greedy Initialization for gbest ===
    gov = greedy_initialization(tasks, vm_mips)
    gbest = gov.copy()
    gct = compute_makespan(gov, tasks, vm_mips)
    gbest_fit = 1.0 / gct

    # === PSO Main Loop ===
    for it in range(max_iter):
        for i in range(num_particles):
            # Update velocity and position
            for d in range(num_tasks):
                r1, r2 = random.random(), random.random()
                velocities[i][d] = (
                    inertia_weight * velocities[i][d]
                    + c1 * r1 * (pbest[i][d] - particles[i][d])
                    + c2 * r2 * (gbest[d] - particles[i][d])
                )
                # Clamp velocity
                velocities[i][d] = max(-(num_vms - 1), min(num_vms - 1, velocities[i][d]))

                # Update position
                new_pos = particles[i][d] + velocities[i][d]
                # Round and clamp to valid VM index
                new_pos = int(round(new_pos))
                new_pos = max(0, min(num_vms - 1, new_pos))
                particles[i][d] = new_pos

            # Evaluate fitness
            makespan = compute_makespan(particles[i], tasks, vm_mips)
            fitness = 1.0 / makespan

            # Update pbest
            if fitness > pbest_fit[i]:
                pbest[i] = particles[i].copy()
                pbest_fit[i] = fitness

            # Update gbest (only if better than greedy initial)
            if fitness > gbest_fit:
                gbest = particles[i].copy()
                gbest_fit = fitness

        if logger and it % 50 == 0:
            logger.log(f"G&PSO Iter {it}: best makespan = {1.0/gbest_fit:.2f}s")

    # === Final schedule: gbest ===
    final_schedule_vm_names = [vm_names[idx] for idx in gbest]

    # === Now EXECUTE the best schedule on real Docker containers ===
    task_events = []
    for i, vm in enumerate(final_schedule_vm_names):
        msg = f"G&PSO: Task {i} ({tasks[i]:.2f} MI) → {vm}"
        if logger:
            logger.log(msg)
        else:
            print(msg)
        # ✅ Correct
        result = run_tasks_parallel([(i, vm, tasks[i])], logger)[0]
        start = result["start"]
        end = result["end"]
        task_events.append({
            "task_id": i,
            "duration": tasks[i],
            "vm": vm,
            "start": start,
            "end": end
        })

    return task_events

run_g_pso_2 = run_g_pso