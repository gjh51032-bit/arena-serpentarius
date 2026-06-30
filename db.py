from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///./game.db")
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
