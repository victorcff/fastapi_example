from typing import Annotated
from fastapi import APIRouter, Depends, Path, Response, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schemas import FeederDeviceRequest, FeederDeviceResponse
from app.models.feeder_devices import FeederDevice
from app.mqtt_client.pub import run as pub_mqtt
from app.mqtt_client.sub import run as sub_mqtt
from app.repositories.feeder_device_repository import FeederDeviceRepository
from app.mqtt_client.constants import main_topic, realtime_weight_subtopic, realtime_weight_response_subtopic, device_mac_address, device_mac_address_response, reconnect_device_wifi

feeder_devices_router = APIRouter(prefix="/feeder-devices")

@feeder_devices_router.get("/weight", summary="Get weigth")
def get_weight():
  pub_mqtt("Cade o peso?", realtime_weight_subtopic)
  mqtt_response = sub_mqtt(f"{main_topic}/{realtime_weight_response_subtopic}")
  if mqtt_response[0]:
    response = {"weight": float(mqtt_response[1])}
    return JSONResponse(content=jsonable_encoder(response))
  else:
    raise HTTPException(
      status_code=status.HTTP_424_FAILED_DEPENDENCY,
      detail="Falha ao receber dados do dispositivo"
    )
    
@feeder_devices_router.get("/mac-address", summary="Get mac address")
def get_mac_address():
  pub_mqtt("cade seu mac?", device_mac_address)
  mqtt_response = sub_mqtt(f"{main_topic}/{device_mac_address_response}")
  if mqtt_response[0]:
    response = {"mac_address": mqtt_response[1]}
    return JSONResponse(content=jsonable_encoder(response))
  else:
    raise HTTPException(
      status_code=status.HTTP_424_FAILED_DEPENDENCY,
      detail="Falha ao receber dados do dispositivo"
    )
    
@feeder_devices_router.post("/reconnect-device-wifi", summary="Reconnect device to other WiFi access point")
def reconnect_wifi():
  pub_mqtt("Reconecte", reconnect_device_wifi)
  return "Conecte ao AP do dispositivo"

@feeder_devices_router.get("/{owner_id}", response_model=list[FeederDeviceResponse], summary="Get all feeder devices from user")
def get_feeder_devices(owner_id: int, db: Session = Depends(get_db)):
  feeder_devices = FeederDeviceRepository.find_by_owner_id(db, owner_id)
  return [FeederDeviceResponse.from_orm(device) for device in feeder_devices]

@feeder_devices_router.get("/id/{device_id}", summary="Get feeder device by ID")
def get_feeder_device(device_id: Annotated[int, Path(description="The ID of the device you want to view", gt=0, lt=3)], db: Session = Depends(get_db)):
  feeder_device = FeederDeviceRepository.find_by_id(db, device_id)
  if not feeder_device:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado"
    )
  return FeederDeviceResponse.from_orm(feeder_device)
  
@feeder_devices_router.post("", response_model=FeederDeviceResponse, status_code=status.HTTP_201_CREATED, summary="Create feeder device")
def create_device(request: FeederDeviceRequest, db: Session = Depends(get_db)):
  feeder_device = FeederDeviceRepository.save(db, FeederDevice(**request.model_dump()))
  return FeederDeviceResponse.model_validate(feeder_device)

@feeder_devices_router.put("/name/{id}", summary="Update feeder device name by ID", response_model=FeederDeviceResponse)
def update(device_id: int, request: FeederDeviceRequest, db: Session = Depends(get_db)):
    if not FeederDeviceRepository.exists_by_id(db, device_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado"
        )
    device = FeederDeviceRepository.save(db, FeederDevice(id=device_id, **request.dict()))
    return FeederDeviceResponse.from_orm(device)

@feeder_devices_router.delete("/{id}", summary="Delete feeder device", status_code=status.HTTP_200_OK, response_model=FeederDeviceResponse)
def delete_by_id(id: int, db: Session = Depends(get_db)):
  if not FeederDeviceRepository.exists_by_id(db, id):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado"
    )
  deleted_feeder_device = FeederDeviceRepository.delete_by_id(db, id)
  return deleted_feeder_device

# Response(status_code=status.HTTP_200_OK, content="Dispositivo excluido com sucesso!")