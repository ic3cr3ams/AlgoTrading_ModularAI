# modules/confidence_module.py

class ConfidenceModule:
    def __init__(self, base_confidence=0.5, decay=0.01, boost=0.05, min_conf=0.0, max_conf=1.0):
        self.confidence = base_confidence
        self.decay = decay
        self.boost = boost
        self.min_conf = min_conf
        self.max_conf = max_conf

    def update(self, reward: float, correct: bool):
        """
        Update confidence berdasarkan hasil keputusan.
        """
        if correct:
            self.confidence += reward * self.boost
        else:
            self.confidence -= reward * self.decay

        self.confidence = max(self.min_conf, min(self.confidence, self.max_conf))

    def get_confidence(self) -> float:
        """
        Ambil nilai confidence saat ini.
        """
        return self.confidence

    def force_penalty(self, amount=0.1):
        """
        Paksa penurunan confidence, digunakan jika AI terlalu sering ganti arah.
        """
        self.confidence -= amount
        self.confidence = max(self.min_conf, self.confidence)

    def reset(self, value=None):
        """
        Reset confidence ke nilai tertentu atau default.
        """
        self.confidence = value if value is not None else 0.5
