from sqlalchemy.orm import Session

from app.models.feeder_devices import FeederDevice

class FeederDeviceRepository:
    @staticmethod
    def find_all(db: Session) -> list[FeederDevice]:
        return db.query(FeederDevice).all()

    @staticmethod
    def  save(db: Session, feeder_device: FeederDevice) -> FeederDevice:
        if feeder_device.id:
            db.merge(feeder_device)
        else:
            db.add(feeder_device)
        db.commit()
        return feeder_device

    @staticmethod
    def find_by_id(db: Session, id: int) -> FeederDevice:
        return db.query(FeederDevice).filter(FeederDevice.id == id).first()
    
    @staticmethod
    def find_by_owner_id(db: Session, owner_id: int) -> FeederDevice:
        return db.query(FeederDevice).filter(FeederDevice.owner_id == owner_id).all()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(FeederDevice).filter(FeederDevice.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> FeederDevice:
        feeder_device = db.query(FeederDevice).filter(FeederDevice.id == id).first()
        if feeder_device is not None:
            db.delete(feeder_device)
            db.commit()
        return feeder_device
