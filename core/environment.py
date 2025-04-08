# core/environment.py

class TradingEnvironment:
    def __init__(self):
        self.current_state = None
        self.last_price = None

    def reset(self, state):
        """
        Mulai episode baru dengan state awal.
        """
        self.current_state = state
        self.last_price = state["close"]
        return self.current_state

    def step(self, action: str, next_price: float):
        """
        Proses aksi AI, evaluasi hasil, dan beri reward.
        """
        reward = 0
        done = False

        if action == "BUY":
            reward = next_price - self.last_price  # profit jika harga naik
        elif action == "WAIT":
            reward = -0.1  # penalti kecil karena pasif
        elif action == "HOLD":
            reward = -abs(next_price - self.last_price) * 0.2  # risiko sideways

        done = True  # untuk saat ini satu step = satu episode
        result = {
            "next_price": next_price,
            "reward": reward,
            "done": done
        }

        return result
