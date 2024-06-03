from typing import Annotated
from fastapi import APIRouter, Depends, Path, status, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schemas import MealsRequest, MealsResponse
from app.models.meals import Meal
from app.repositories.meals_repository import MealsRepository
from app.mqtt_client.pub import run as pub_mqtt
from app.mqtt_client.constants import activate_meal

meals_router = APIRouter(prefix="/meals")

@meals_router.get("/{feeder_device_id}", response_model=list[MealsResponse], summary="Get all meals from feeder device")
def get_meals(feeder_device_id: int, db: Session = Depends(get_db)):
  meals = MealsRepository.find_by_owner_id(db, feeder_device_id)
  return [MealsResponse.from_orm(meal) for meal in meals]

@meals_router.get("/id/{meal_id}", summary="Get meal by ID")
def get_meal(meal_id: Annotated[int, Path(description="The ID of the meal you want to view", gt=0, lt=3)], db: Session = Depends(get_db)):
  meal = MealsRepository.find_by_id(db, meal_id)
  if not meal:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Refeição não encontrada"
    )
  return MealsResponse.from_orm(meal)
  
@meals_router.post("", response_model=MealsResponse, status_code=status.HTTP_201_CREATED, summary="Create meal")
def create_meal(request: MealsRequest, db: Session = Depends(get_db)):
  meal_data = request.dict()
  meal = Meal(**meal_data)
  saved_meal = MealsRepository.save(db, meal)
  return MealsResponse.from_orm(saved_meal)

@meals_router.post("/activate-meal", status_code=status.HTTP_200_OK, summary="Activate meal")
def activate_meal_mqtt():
  pub_mqtt("Ativar refeicao", activate_meal)
  return 

@meals_router.put("/id/{meal_id}", summary="Update meal by ID", response_model=MealsResponse)
def update(meal_id: int, request: MealsRequest, db: Session = Depends(get_db)):
    if not MealsRepository.exists_by_id(db, meal_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Refeição não encontrada"
        )
    meal = MealsRepository.save(db, Meal(id=meal_id, **request.dict()))
    return MealsResponse.from_orm(meal)

@meals_router.delete("/{id}", summary="Delete meal", status_code=status.HTTP_200_OK, response_model=MealsResponse)
def delete_by_id(id: int, db: Session = Depends(get_db)):
  if not MealsRepository.exists_by_id(db, id):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Refeição não encontrada"
    )
  delete_meal = MealsRepository.delete_by_id(db, id)
  return delete_meal

# Response(status_code=status.HTTP_200_OK, content="Dispositivo excluido com sucesso!")