from sqlalchemy.orm import Session

from app.models.meals import Meal

class MealsRepository:
    @staticmethod
    def find_all(db: Session) -> list[Meal]:
        return db.query(Meal).all()

    @staticmethod
    def  save(db: Session, meal: Meal) -> Meal:
        if meal.id:
            db.merge(meal)
        else:
            db.add(meal)
        db.commit()
        return meal

    @staticmethod
    def find_by_id(db: Session, id: int) -> Meal:
        return db.query(Meal).filter(Meal.id == id).first()
    
    @staticmethod
    def find_by_owner_id(db: Session, device_id: int) -> Meal:
        return db.query(Meal).filter(Meal.device_id == device_id).all()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Meal).filter(Meal.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> Meal:
        meal = db.query(Meal).filter(Meal.id == id).first()
        if meal is not None:
            db.delete(meal)
            db.commit()
        return meal
