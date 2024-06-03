from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base

class Meal(Base):
  __tablename__ = "meals"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(50), nullable=False, unique=True)
  device_id = Column(Integer, ForeignKey("feeder_devices.id"))
  weight = Column(String(20), nullable=False)
  time = Column(String(10), nullable=False)