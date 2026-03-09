from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class ViolationEvent(Base):
    __tablename__ = "violation_events"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    vehicle_label = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    violation_type = Column(String, nullable=False)
    evidence_url = Column(String, nullable=True)
    bbox = Column(String, nullable=False)
    plate_text = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, nullable=True)

    camera = relationship("Camera")


class DailySummary(Base):
    __tablename__ = "daily_summary"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, unique=True)
    total_violations = Column(Integer, nullable=False, default=0)
    red_light_count = Column(Integer, nullable=False, default=0)
    lane_violation_count = Column(Integer, nullable=False, default=0)
    avg_confidence = Column(Float, nullable=False, default=0.0)
