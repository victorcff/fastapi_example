from typing import Annotated
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.database.schemas import UserCreate, UserResponse, UserRequest
from sqlalchemy.orm import Session
from app.database.db import get_db
from fastapi import Depends, APIRouter, HTTPException, Path, Response, status 

users_router = APIRouter(prefix="/user")

@users_router.get("/", summary="Get all users")
def get_user(db: Session = Depends(get_db)):
  users = UserRepository.find_all(db)
  return [UserResponse.from_orm(user) for user in users]

@users_router.get("/id/{user_id}", summary="Get user by ID")
def get_user_by_id(user_id: Annotated[int, Path(description="The ID of the user you want to view", gt=0, lt=3)], db: Session = Depends(get_db)):
  user = UserRepository.find_by_id(db, user_id)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
    )
  return UserResponse.from_orm(user)
  
@users_router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create user")
def create_user(request: UserCreate, db: Session = Depends(get_db)):
  try:
    user = UserRepository.save(db, User(**request.model_dump()))
  except:
    raise HTTPException(
      status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Nome de usuário já existente."
    )
  return UserResponse.model_validate(user)

@users_router.post("/auth", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Authenticate user")
def authenticate_user(request: UserCreate, db: Session = Depends(get_db)):
  valid_user = UserRepository.validate_password(db, request.username, request.password)
  if not valid_user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos!"
    )
  return UserResponse.model_validate(valid_user)

@users_router.put("/name/{id}", summary="Update user name by ID", response_model=UserResponse)
def update(user_id: int, request: UserRequest, db: Session = Depends(get_db)):
    if not UserRepository.exists_by_id(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )
    user = UserRepository.save(db, User(id=user_id, **request.dict()))
    return UserResponse.from_orm(user)

@users_router.delete("/{id}", summary="Delete user", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(user_id: int, db: Session = Depends(get_db)):
  if not UserRepository.exists_by_id(db, user_id):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
    )
  UserRepository.delete_by_id(db, user_id)
  return Response(status_code=status.HTTP_204_NO_CONTENT)