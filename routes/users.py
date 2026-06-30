from fastapi import APIRouter
from db import SessionLocal
from models import User
from services.game_service import update_energy

router = APIRouter()

@router.get("/me")
def get_me(telegram_id: str):
    db = SessionLocal()

    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        db.close()
        return {"error": "User not found"}

    update_energy(user)
    db.commit()

    data = {
        "telegram_id": user.telegram_id,
        "points": user.points,
        "xp": user.xp,
        "level": user.level,
        "energy": user.energy
    }

    db.close()

    return data

@router.post("/create_user")
def create_user(telegram_id: str):
    db = SessionLocal()

    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    data = {
        "telegram_id": user.telegram_id,
        "points": user.points,
        "xp": user.xp,
        "level": user.level,
        "energy": user.energy
    }

    db.close()

    return data
