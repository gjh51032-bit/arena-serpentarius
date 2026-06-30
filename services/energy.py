import asyncio
from db import SessionLocal
from models import User

MAX_ENERGY = 1000
REGEN_AMOUNT = 1
REGEN_TIME = 7  # 5–10 сек баланс

async def energy_regeneration():
    while True:
        db = SessionLocal()

        users = db.query(User).all()

        for user in users:
            if user.energy < MAX_ENERGY:
                user.energy += REGEN_AMOUNT
                if user.energy > MAX_ENERGY:
                    user.energy = MAX_ENERGY

        db.commit()
        db.close()

        await asyncio.sleep(REGEN_TIME)

