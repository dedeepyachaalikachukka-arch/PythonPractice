from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.violation import ViolationEvent
from app.schemas.violation import ViolationRead

router = APIRouter()


@router.get("/", response_model=list[ViolationRead])
def list_violations(db: Session = Depends(get_db)):
    return db.query(ViolationEvent).order_by(ViolationEvent.created_at.desc()).all()


@router.get("/{violation_id}", response_model=ViolationRead)
def get_violation(violation_id: int, db: Session = Depends(get_db)):
    violation = db.query(ViolationEvent).filter(ViolationEvent.id == violation_id).first()
    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")
    return violation
