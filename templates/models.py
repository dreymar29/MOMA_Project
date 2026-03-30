from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

db_url = "sqlite:///database.db"

engine = create_engine(db_url)

Base = declarative_base()

class Art(Base):
    __tablename__ = "art"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

