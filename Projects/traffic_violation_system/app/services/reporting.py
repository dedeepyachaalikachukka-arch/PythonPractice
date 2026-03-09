from __future__ import annotations

from collections import defaultdict
from statistics import mean

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.violation import DailySummary, ViolationEvent


def refresh_daily_summary(db: Session) -> None:
    events = db.query(ViolationEvent).all()
    grouped: dict = defaultdict(list)
    for event in events:
        grouped[event.created_at.date()].append(event)

    db.query(DailySummary).delete()
    db.commit()

    for day, items in grouped.items():
        summary = DailySummary(
            date=day,
            total_violations=len(items),
            red_light_count=sum(1 for item in items if item.violation_type == "red_light"),
            lane_violation_count=sum(1 for item in items if item.violation_type == "lane_violation"),
            avg_confidence=float(mean(item.confidence for item in items)),
        )
        db.add(summary)
    db.commit()


def violation_count(db: Session) -> int:
    return int(db.query(func.count(ViolationEvent.id)).scalar() or 0)
