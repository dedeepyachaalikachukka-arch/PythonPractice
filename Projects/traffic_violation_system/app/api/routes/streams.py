from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.camera import Camera
from app.schemas.camera import CameraCreate, CameraRead
from app.schemas.violation import AnalyzeResponse
from app.services.processor import process_camera_stream

router = APIRouter()


@router.post("/register", response_model=CameraRead)
def register_camera(payload: CameraCreate, db: Session = Depends(get_db)):
    camera = Camera(**payload.model_dump())
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera


@router.get("/", response_model=list[CameraRead])
def list_cameras(db: Session = Depends(get_db)):
    return db.query(Camera).all()


@router.post("/{camera_id}/analyze", response_model=AnalyzeResponse)
def analyze_stream(camera_id: int, db: Session = Depends(get_db)):
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return process_camera_stream(db=db, camera=camera)
