# modules/market_structure_module.py

class MarketStructureModule:
    def __init__(self):
        self.last_high = None
        self.last_low = None
        self.last_structure = "unknown"

    def update(self, current_high, current_low):
        """
        Update struktur pasar berdasarkan high & low baru.
        """
        if self.last_high is None or self.last_low is None:
            self.last_high = current_high
            self.last_low = current_low
            self.last_structure = "unknown"
            return self.last_structure

        if current_high > self.last_high and current_low > self.last_low:
            structure = "uptrend"
        elif current_high < self.last_high and current_low < self.last_low:
            structure = "downtrend"
        else:
            structure = "sideways"

        self.last_high = current_high
        self.last_low = current_low
        self.last_structure = structure

        return structure

    def get_structure(self):
        """
        Ambil struktur terakhir.
        """
        return self.last_structure
