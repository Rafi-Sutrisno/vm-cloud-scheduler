# utils/stats_logger.py
import subprocess
import time
import csv
import os

class DockerStatsLogger:
    def __init__(self, exp_dir, vm_names, algo_name):
        self.exp_dir = exp_dir
        self.vm_names = vm_names
        self.stats_file = os.path.join(exp_dir, f"docker_stats_{algo_name}.csv")
        with open(self.stats_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "container", "cpu_percent", "mem_usage"])

    def log_stats(self):
        try:
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format", "{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            if not output:
                return

            lines = output.split("\n")
            timestamp = time.time()
            with open(self.stats_file, "a", newline="") as f:
                writer = csv.writer(f)
                for line in lines:
                    parts = line.split("\t")
                    if len(parts) >= 3:
                        container = parts[0]
                        cpu = parts[1].rstrip('%')
                        mem_usage = parts[2]
                        writer.writerow([timestamp, container, cpu, mem_usage])
        except subprocess.TimeoutExpired:
            print("Docker stats command timed out.")
        except Exception as e:
            print(f"Error logging stats: {e}")