from sqlalchemy import text

from app.db.session import SessionLocal, init_db
from app.models.violation import ViolationEvent
from app.services.reporting import refresh_daily_summary


def test_refresh_daily_summary() -> None:
    init_db()
    db = SessionLocal()
    db.query(ViolationEvent).delete()
    db.commit()

    db.add(
        ViolationEvent(
            camera_id=1,
            vehicle_label="car",
            confidence=0.9,
            violation_type="red_light",
            evidence_url="file.jpg",
            bbox="(1,2,3,4)",
        )
    )
    db.commit()
    refresh_daily_summary(db)
    summaries = db.execute(text("SELECT total_violations FROM daily_summary")).fetchall()
    assert summaries
    db.close()
