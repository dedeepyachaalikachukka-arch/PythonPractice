from __future__ import annotations

import cv2
from sqlalchemy.orm import Session

from app.models.camera import Camera
from app.models.violation import ViolationEvent
from app.schemas.violation import AnalyzeResponse, ViolationRead
from app.services.detector import get_detector
from app.services.storage import EvidenceStorage
from app.services.violation_logic import classify_violation


def process_camera_stream(db: Session, camera: Camera, max_frames: int = 30) -> AnalyzeResponse:
    detector = get_detector()
    storage = EvidenceStorage()
    cap = cv2.VideoCapture(camera.source_url)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open source: {camera.source_url}")

    processed_frames = 0
    created_events: list[ViolationEvent] = []

    while processed_frames < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        processed_frames += 1

        detections = detector.detect(frame)
        for det in detections:
            is_violation, violation_type, notes = classify_violation(camera, det, processed_frames)
            if not is_violation:
                continue
            evidence_url = storage.save_frame(frame, camera.id)
            event = ViolationEvent(
                camera_id=camera.id,
                vehicle_label=det.label,
                confidence=det.confidence,
                violation_type=violation_type,
                evidence_url=evidence_url,
                bbox=str(det.bbox),
                plate_text="UNKNOWN",
                notes=notes,
            )
            db.add(event)
            db.flush()
            created_events.append(event)

    db.commit()
    for event in created_events:
        db.refresh(event)
    cap.release()

    return AnalyzeResponse(
        processed_frames=processed_frames,
        events_created=len(created_events),
        violations=[ViolationRead.model_validate(event) for event in created_events],
    )
