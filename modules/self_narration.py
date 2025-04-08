# modules/self_narration.py

import datetime

class SelfNarrationEngine:
    def __init__(self):
        self.logs = []

    def narrate(self, state, action, structure, napas_status, confidence, reward):
        """
        Buat narasi sederhana berdasarkan input keputusan.
        """
        timestamp = datetime.datetime.utcnow().isoformat()

        narration = {
            "time": timestamp,
            "state_summary": {
                "close": state.get("close"),
                "atr_h1": state.get("atr_h1"),
                "structure": structure,
                "napas": {
                    "H1": napas_status.get("H1"),
                    "H4": napas_status.get("H4"),
                    "D1": napas_status.get("D1")
                }
            },
            "decision": {
                "action": action,
                "confidence": confidence,
                "reward": reward
            },
            "reflection": self._reflect(action, confidence, reward)
        }

        self.logs.append(narration)
        return narration

    def _reflect(self, action, confidence, reward):
        """
        Narasi pendek tentang kondisi mental AI
        """
        if reward > 0:
            tone = "Saya mengambil aksi '{}' dengan keyakinan {:.2f} dan hasilnya positif.".format(action, confidence)
        elif reward < 0:
            tone = "Saya mengambil aksi '{}' dengan keyakinan {:.2f}, namun hasilnya negatif.".format(action, confidence)
        else:
            tone = "Saya memilih '{}' tapi hasilnya netral.".format(action)

        if confidence > 0.7:
            tone += " Saya cukup yakin tadi."
        elif confidence < 0.3:
            tone += " Saya agak ragu saat itu."

        return tone

    def get_last_narration(self):
        return self.logs[-1] if self.logs else None

    def export_log(self):
        """
        (Opsional) kamu bisa simpan semua narasi ke file nanti.
        """
        return self.logs
