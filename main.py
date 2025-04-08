# main.py

from core.decision_engine import DecisionEngine
from core.environment import TradingEnvironment
from utils.logger import TradingLogger

# Inisialisasi modul utama dan logger
engine = DecisionEngine()
env = TradingEnvironment()
logger = TradingLogger()

# Contoh data dummy untuk 1 episode
state = {
    "high": 1.1820,
    "low": 1.1720,
    "close": 1.1750,
    "recent_low": 1.1500,
    "atr_h1": 12.0,
    "atr_h4": 22.5,
    "atr_d1": 40.0
}

# Jalankan environment
env.reset(state)

# Ambil keputusan AI
action = engine.make_decision(state, result={})
print(f"Aksi AI: {action}")

# Simulasikan next price (contoh)
next_price = 1.1800

# Evaluasi hasil aksi
result = env.step(action, next_price)

# Update confidence AI (jika kamu mau)
engine.confidence.update(
    reward=result["reward"],
    correct=result["reward"] > 0  # dianggap benar jika reward positif
)

# Simpan memori
engine.memory.store(state, action, result)

# Log setiap aksi dan refleksi narasi
logger.log(
    state=state,
    action=action,
    confidence=engine.confidence.get_confidence(),
    reward=result["reward"],
    narration=engine.narrator.get_last_narration()
)

print(f"Reward: {result['reward']}")
