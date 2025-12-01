# utils/logger.py
import os
from datetime import datetime

class ExperimentLogger:
    def __init__(self, exp_dir):
        self.log_file = os.path.join(exp_dir, "schedule_log.txt")
        with open(self.log_file, "w", encoding="utf-8") as f:
            pass  

    def log(self, message):
        print(message)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")