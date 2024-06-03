from sqlalchemy.orm import Session
from app.models.users import User
import hashlib

class UserRepository:
    @staticmethod
    def find_all(db: Session) -> list[User]:
        return db.query(User).all()

    @staticmethod
    def save(db: Session, user: User) -> User:
        user.password = hashlib.sha256(user.password.encode('utf8')).hexdigest()
        if user.id:
            db.merge(user)
        else:
            db.add(user)
        db.commit()
        return user

    @staticmethod
    def find_by_id(db: Session, id: int) -> User:
        return db.query(User).filter(User.id == id).first()
    
    @staticmethod
    def find_by_name(db: Session, name: str) -> User:
        return db.query(User).filter(User.username == name).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(User).filter(User.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        user = db.query(User).filter(User.id == id).first()
        if user is not None:
            db.delete(user)
            db.commit()
            
    @staticmethod
    def validate_password(db: Session, name: str, password: str):
        user = UserRepository.find_by_name(db, name)
        if not user:
            return None
        hashed_password = hashlib.sha256(password.encode('utf8')).hexdigest()
        if user.password == hashed_password:
            return user
        return None
