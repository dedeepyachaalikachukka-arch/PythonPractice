from __future__ import annotations

from app.models.camera import Camera
from app.services.detector import Detection


def infer_signal_state(frame_index: int) -> str:
    return "red" if frame_index % 2 == 0 else "green"


def classify_violation(camera: Camera, detection: Detection, frame_index: int) -> tuple[bool, str, str | None]:
    x, y, w, h = detection.bbox
    bottom_y = y + h
    signal_state = infer_signal_state(frame_index)

    if camera.stop_line_y is not None and signal_state == "red" and bottom_y > camera.stop_line_y:
        return True, "red_light", f"Vehicle crossed stop line at y={camera.stop_line_y} during red signal"

    if x < 20:
        return True, "lane_violation", "Vehicle entered restricted lane boundary"

    return False, "", None
