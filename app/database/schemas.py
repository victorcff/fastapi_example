from pydantic import BaseModel
from typing import List, Optional

class MealsBase(BaseModel):
  device_id: int
  time: str
  weight: float
  name: str
  class Config:
    orm_mode = True
    from_attributes = True
  
class MealsRequest(MealsBase):
  ...

class MealsResponse(MealsBase):
  id: int
  # class Config:
  #   orm_mode = True
  #   from_attributes: True
    
class MealsCreate(MealsBase):
  ...

class FeederDeviceBase(BaseModel):
  name: str
  owner_id: int
  mac_address: str
  
class FeederDeviceCreate(FeederDeviceBase):
  ...

class FeederDeviceRequest(FeederDeviceBase):
  ...

class FeederDeviceResponse(FeederDeviceBase):
  id: int
  meals: List[MealsResponse]
  class Config:
    orm_mode = True
    from_attributes = True
    
class UserBase(BaseModel):
  username: str
  
class UserCreate(UserBase):
  password: str
  
class UserResponse(UserBase):
  id: int
  feeder_devices: List[FeederDeviceResponse]
  class Config:
    orm_mode = True
    from_attributes = True
    
class UserRequest(UserBase):
  ...

# class User(UserBase):
#   id: int
#   is_active: bool
#   feeder_devices: List[FeederDeviceResponse] = []

