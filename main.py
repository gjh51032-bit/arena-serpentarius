import asyncio
from db import Base, engine
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import SessionLocal
from models import User

Base.metadata.create_all(bind=engine)

from routes.users import router as users_router
from routes.game import router as game_router
from services.energy import energy_regeneration

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

app.include_router(users_router)
app.include_router(game_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(energy_regeneration())

@app.get("/")
def home():
    return {"status": "Arena Serpentarius API is running"}

@app.post("/create_user")
def create_user(telegram_id: str):
    db = SessionLocal()

    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    return {
        "telegram_id": user.telegram_id,
        "points": user.points,
        "level": user.level,
        "energy": user.energy
    }



