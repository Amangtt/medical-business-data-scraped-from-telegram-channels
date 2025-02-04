import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, get_db, DATABASE_URL
print(f"DATABASE_URL: {DATABASE_URL}")

# Create database tables
models.Base.metadata.create_all(bind=engine)


# Initialize FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Medical Business API"}

# 🔹 Medical Businesses Endpoints
@app.post("/medical_businesses/", response_model=schemas.MedicalBusinessCreate)
def create_medical_business(business: schemas.MedicalBusinessCreate, db: Session = Depends(get_db)):
    return crud.create_medical_business(db=db, business=business)

@app.get("/medical_businesses/", response_model=list[schemas.MedicalBusinessResponse])
def read_medical_businesses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_medical_businesses(db, skip=skip, limit=limit)

@app.get("/medical_businesses/{business_id}", response_model=schemas.MedicalBusinessResponse)
def read_medical_business(business_id: int, db: Session = Depends(get_db)):
    db_business = crud.get_medical_business(db, business_id=business_id)
    if db_business is None:
        raise HTTPException(status_code=404, detail="Medical business not found")
    return db_business

# 🔹 Object Detection Endpoints
@app.post("/object_detections/", response_model=schemas.ObjectDetectionCreate)
def create_object_detection(detection: schemas.ObjectDetectionCreate, db: Session = Depends(get_db)):
    return crud.create_object_detection(db=db, detection=detection)

@app.get("/object_detections/", response_model=list[schemas.ObjectDetectionResponse])
def read_object_detections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_object_detections(db, skip=skip, limit=limit)

@app.get("/object_detections/{detection_id}", response_model=schemas.ObjectDetectionResponse)
def read_object_detection(detection_id: int, db: Session = Depends(get_db)):
    db_detection = crud.get_object_detection(db, detection_id=detection_id)
    if db_detection is None:
        raise HTTPException(status_code=404, detail="Object detection record not found")
    return db_detection

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
