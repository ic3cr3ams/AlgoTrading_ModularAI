# modules/napas_pasar_module.py

class NapasPasarModule:
    def __init__(self, tension_threshold=1.5, explosion_threshold=2.0):
        self.atr_values = {}
        self.previous_atr_values = {}
        self.status = {}  # per timeframe
        self.tension_threshold = tension_threshold
        self.explosion_threshold = explosion_threshold

    def update_atr(self, timeframe: str, new_atr: float):
        """
        Update nilai ATR berdasarkan timeframe.
        """
        if timeframe in self.atr_values:
            self.previous_atr_values[timeframe] = self.atr_values[timeframe]

        self.atr_values[timeframe] = new_atr
        self._evaluate_tension(timeframe)

    def _evaluate_tension(self, timeframe: str):
        prev = self.previous_atr_values.get(timeframe)
        curr = self.atr_values.get(timeframe)

        if prev is None or curr is None or prev == 0:
            self.status[timeframe] = "normal"
            return

        ratio = curr / prev

        if ratio >= self.explosion_threshold:
            self.status[timeframe] = "meledak"
        elif ratio >= self.tension_threshold:
            self.status[timeframe] = "memanas"
        else:
            self.status[timeframe] = "tenang"

    def get_napas_status(self, timeframe: str):
        return self.status.get(timeframe, "unknown")

    def get_overall_pressure(self):
        """
        Evaluasi kombinasi semua timeframe (opsional)
        """
        explosive = [tf for tf, stat in self.status.items() if stat == "meledak"]
        if len(explosive) >= 2:
            return "kritis"
        elif any(stat == "memanas" for stat in self.status.values()):
            return "waspada"
        else:
            return "normal"

    def check_strong_bullish_potential(self, current_price: float, recent_low: float) -> bool:
        """
        Deteksi peluang strong bullish:
        - ATR naik serempak di H1, H4, D1
        - Harga masih dekat recent low (belum breakout)
        """
        tf_check = ["H1", "H4", "D1"]
        atr_up = all(
            self.atr_values.get(tf) and self.previous_atr_values.get(tf) and
            self.atr_values[tf] > self.previous_atr_values[tf]
            for tf in tf_check
        )

        price_position_ok = current_price <= (recent_low * 1.10)  # masih dekat low

        return atr_up and price_position_ok
