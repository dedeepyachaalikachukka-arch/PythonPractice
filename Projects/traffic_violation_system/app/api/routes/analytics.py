from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.violation import DailySummary
from app.schemas.violation import DailySummaryRead
from app.services.reporting import refresh_daily_summary

router = APIRouter()


@router.post("/refresh", response_model=list[DailySummaryRead])
def refresh_summary(db: Session = Depends(get_db)):
    refresh_daily_summary(db)
    return db.query(DailySummary).order_by(DailySummary.date.desc()).all()


@router.get("/daily-summary", response_model=list[DailySummaryRead])
def daily_summary(db: Session = Depends(get_db)):
    return db.query(DailySummary).order_by(DailySummary.date.desc()).all()
