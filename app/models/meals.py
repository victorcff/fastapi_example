from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base

class Meal(Base):
  __tablename__ = "meals"
  id: int = Column(Integer, primary_key=True, index=True)
  name: str = Column(String(50), nullable=False)
  device_id: int = Column(Integer, ForeignKey("feeder_devices.id"))
  weight: str = Column(String(20), nullable=False)
  time: str = Column(String(10), nullable=False)