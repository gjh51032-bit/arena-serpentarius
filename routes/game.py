from services.levels import calculate_level
from fastapi import APIRouter
from db import SessionLocal
from models import User
from services.game_service import tap_user

router = APIRouter()


@router.post("/tap")
def tap(telegram_id: str):
    return tap_user(telegram_id)
