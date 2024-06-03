from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base

class FeederDevice(Base):
  __tablename__ = "feeder_devices"
  id: int = Column(Integer, primary_key=True, index=True)
  name: str = Column(String(50), nullable=False)
  owner_id: int = Column(Integer, ForeignKey("users.id"))
  mac_address: str = Column(String(20), nullable=False, unique=True)
  meals = relationship("Meal", backref="feeder_device")
  