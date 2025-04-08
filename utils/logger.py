# utils/logger.py

import json
import os
from datetime import datetime

class TradingLogger:
    def __init__(self, log_dir="logs", filename_prefix="ai_log"):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(log_dir, f"{filename_prefix}_{timestamp}.json")
        self.logs = []

    def log(self, state, action, confidence, reward, narration=None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "state": state,
            "action": action,
            "confidence": confidence,
            "reward": reward,
            "narration": narration
        }
        self.logs.append(log_entry)
        self._save()

    def _save(self):
        with open(self.log_path, 'w') as f:
            json.dump(self.logs, f, indent=2)

    def get_all_logs(self):
        return self.logs
