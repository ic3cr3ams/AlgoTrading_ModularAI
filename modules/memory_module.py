# modules/memory_module.py

import json
import os
from collections import deque
from typing import Dict, Any, List

class MemoryModule:
    def __init__(self, max_memory_size=10000, save_path="data/memory_bank.json"):
        self.memory = deque(maxlen=max_memory_size)
        self.save_path = save_path

    def store(self, state: Dict[str, Any], action: str, result: Dict[str, Any]):
        """
        Simpan satu memori ke dalam sistem
        """
        self.memory.append({
            "state": state,
            "action": action,
            "result": result
        })

    def load_memory(self):
        """
        Muat memori dari file JSON
        """
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r') as f:
                data = json.load(f)
                self.memory = deque(data, maxlen=self.memory.maxlen)

    def save_memory(self):
        """
        Simpan seluruh memori ke file JSON
        """
        with open(self.save_path, 'w') as f:
            json.dump(list(self.memory), f, indent=2)

    def find_resonance(self, current_state: Dict[str, Any], threshold=0.8) -> List[Dict[str, Any]]:
        """
        Cari pola historis yang mirip dengan current_state berdasarkan kemiripan sederhana
        """
        resonant_memories = []
        for memory in self.memory:
            similarity = self._calculate_similarity(current_state, memory['state'])
            if similarity >= threshold:
                resonant_memories.append({
                    "memory": memory,
                    "similarity": similarity
                })
        return resonant_memories

    def _calculate_similarity(self, state1: Dict[str, Any], state2: Dict[str, Any]) -> float:
        """
        Hitung kemiripan sederhana antar 2 state
        """
        keys = list(state1.keys())
        matches = sum(1 for key in keys if key in state2 and state1[key] == state2[key])
        return matches / len(keys) if keys else 0.0
