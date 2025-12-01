# visualize_vms.py
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

load_dotenv()

VM_CONFIG = {
    "vm1": float(os.getenv("VM1_CPUS")),
    "vm2": float(os.getenv("VM2_CPUS")),
    "vm3": float(os.getenv("VM3_CPUS")),
    "vm4": float(os.getenv("VM4_CPUS")),
    "vm5": float(os.getenv("VM5_CPUS")),
}

def plot_vms(vm_config, save_path="./storage/vms/vm_capacity.png"):
    vms = list(vm_config.keys())
    cpus = list(vm_config.values())

    plt.figure(figsize=(8, 4))
    bars = plt.bar(vms, cpus, color='lightgreen', edgecolor='black')
    plt.title("Virtual Machine CPU Capacity (Relative)")
    plt.ylabel("CPU Quota (cores)")
    plt.ylim(0, max(cpus) * 1.2)
    for bar, cpu in zip(bars, cpus):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{cpu}", ha='center')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.savefig(save_path)
    plt.show()
    print(f"✅ VM configuration saved to {save_path}")

if __name__ == "__main__":
    plot_vms(VM_CONFIG)