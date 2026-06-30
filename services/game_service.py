import time
import threading
from db import SessionLocal
from models import User


ENERGY_MAX = 1000
ENERGY_PER_SEC = 1 / 10  # 1 энергия в 10 секунд

COOLDOWN_SECONDS = 5

locks = {}

def update_energy(user):
    now = time.time()

    if user.last_energy_update == 0:
        user.last_energy_update = now
        return

    elapsed = now - user.last_energy_update

    gained_energy = int(elapsed * ENERGY_PER_SEC)

    if gained_energy > 0:
        user.energy += gained_energy

        if user.energy > ENERGY_MAX:
            user.energy = ENERGY_MAX

        user.last_energy_update = now

def tap_user(telegram_id: str):
    db = SessionLocal()

    global locks

    if telegram_id not in locks:
        locks[telegram_id] = threading.Lock()

    lock = locks[telegram_id]

    with lock:

        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        if not user:
            db.close()
            return {"error": "User not found"}

        update_energy(user)

        now = time.time()

    # cooldown check
        if user.last_tap > 0 and (now - user.last_tap < 5):
            db.close()
            return {"error": "Cooldown active",
                "wait": round(5 - (now - user.last_tap), 2)
            }

        if user.energy <= 0:
            db.close()
            return {"error": "No energy"}

    # rewards
        user.points += 1
        user.xp += 1
        user.energy -= 1

    # level system
        while user.xp >= user.level * 20:
            user.xp -= user.level * 20
            user.level += 1

        user.last_tap = now

        db.commit()

        result = {
            "points": user.points,
            "xp": user.xp,
            "level": user.level,
            "energy": user.energy
    }

        db.close()
        return result
