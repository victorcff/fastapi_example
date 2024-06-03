from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  username = Column(Text(50), nullable=False, unique=True)
  password = Column(Text(100), nullable=False)
  feeder_devices = relationship(
    "FeederDevice",
    backref="user"
  )
  