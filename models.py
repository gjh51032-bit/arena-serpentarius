from sqlalchemy import Column, Integer, String, Float
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    points = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    energy = Column(Integer, default=1000)
    last_tap = Column(Float, default=0)
    last_energy_update = Column(Float, default=0)
