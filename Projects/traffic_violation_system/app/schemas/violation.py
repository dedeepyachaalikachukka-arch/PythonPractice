from datetime import datetime, date
from pydantic import BaseModel


class ViolationRead(BaseModel):
    id: int
    camera_id: int
    vehicle_label: str
    confidence: float
    violation_type: str
    evidence_url: str | None = None
    bbox: str
    plate_text: str | None = None
    created_at: datetime
    notes: str | None = None

    model_config = {"from_attributes": True}


class AnalyzeResponse(BaseModel):
    processed_frames: int
    events_created: int
    violations: list[ViolationRead]


class DailySummaryRead(BaseModel):
    date: date
    total_violations: int
    red_light_count: int
    lane_violation_count: int
    avg_confidence: float

    model_config = {"from_attributes": True}
