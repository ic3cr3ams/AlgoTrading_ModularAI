# core/decision_engine.py

from modules.memory_module import MemoryModule
from modules.napas_pasar_module import NapasPasarModule
from modules.confidence_module import ConfidenceModule
from modules.market_structure_module import MarketStructureModule
from modules.self_narration import SelfNarrationEngine

class DecisionEngine:
    def __init__(self):
        self.memory = MemoryModule()
        self.napas = NapasPasarModule()
        self.confidence = ConfidenceModule()
        self.market_structure = MarketStructureModule()
        self.narrator = SelfNarrationEngine()

    def make_decision(self, state: dict, result: dict = None) -> str:
        """
        Fungsi utama untuk membuat keputusan berdasarkan state pasar saat ini.
        """
        # Step 1: Update modul
        self.napas.update_atr("H1", state["atr_h1"])
        self.napas.update_atr("H4", state["atr_h4"])
        self.napas.update_atr("D1", state["atr_d1"])

        structure = self.market_structure.update(state["high"], state["low"])
        confidence_score = self.confidence.get_confidence()

        # Step 2: Cek resonance memory
        resonances = self.memory.find_resonance(state, threshold=0.8)

        # Step 3: Evaluasi napas pasar
        strong_bullish = self.napas.check_strong_bullish_potential(
            current_price=state["close"],
            recent_low=state["recent_low"]
        )

        # Step 4: Logika pengambilan keputusan
        if strong_bullish and confidence_score > 0.6 and structure == "uptrend":
            action = "BUY"
        elif confidence_score < 0.3 or structure == "downtrend":
            action = "WAIT"
        else:
            action = "HOLD"

        # Step 5: Simpan ke memori (sementara result bisa kosong atau diisi dari environment)
        self.memory.store(state, action, result or {})

        # Step 6: Narasi AI
        narration = self.narrator.narrate(
            state=state,
            action=action,
            structure=structure,
            napas_status={
                "H1": self.napas.get_napas_status("H1"),
                "H4": self.napas.get_napas_status("H4"),
                "D1": self.napas.get_napas_status("D1")
            },
            confidence=confidence_score,
            reward=result["reward"] if result else 0.0
        )

        print(narration["reflection"])

        return action
