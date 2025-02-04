from sqlalchemy.orm import Session
import models, schemas


# 📌 CRUD for Medical Businesses
def get_medical_business(db: Session, business_id: int):
    """Retrieve a single medical business record by ID."""
    return db.query(models.MedicalBusiness).filter(models.MedicalBusiness.id == business_id).first()


def get_medical_businesses(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve multiple medical business records."""
    return db.query(models.MedicalBusiness).offset(skip).limit(limit).all()


def create_medical_business(db: Session, business: schemas.MedicalBusinessCreate):
    """Create a new medical business record."""
    db_business = models.MedicalBusiness(**business.dict())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


# 📌 CRUD for Object Detection
def get_object_detection(db: Session, detection_id: int):
    """Retrieve a single object detection record by ID."""
    return db.query(models.ObjectDetection).filter(models.ObjectDetection.id == detection_id).first()


def get_object_detections(db: Session, skip: int = 0, limit: int = 10):
    """Retrieve multiple object detection records."""
    return db.query(models.ObjectDetection).offset(skip).limit(limit).all()


def create_object_detection(db: Session, detection: schemas.ObjectDetectionCreate):
    """Create a new object detection record."""
    db_detection = models.ObjectDetection(**detection.dict())
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    return db_detection
