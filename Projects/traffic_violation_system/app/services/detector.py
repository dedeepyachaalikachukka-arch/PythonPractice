from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from app.core.config import settings

VEHICLE_CLASSES = {"car", "bus", "truck", "motorbike"}


@dataclass
class Detection:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]


class BaseDetector:
    def detect(self, frame: np.ndarray) -> list[Detection]:
        raise NotImplementedError


class MockDetector(BaseDetector):
    def detect(self, frame: np.ndarray) -> list[Detection]:
        h, w = frame.shape[:2]
        return [
            Detection(label="car", confidence=0.93, bbox=(w // 4, h // 2, w // 4, h // 4)),
            Detection(label="truck", confidence=0.87, bbox=(w // 2, h // 2 - 20, w // 3, h // 3)),
        ]


class YOLOv2Detector(BaseDetector):
    def __init__(self) -> None:
        cfg = Path(settings.yolo_config_path)
        weights = Path(settings.yolo_weights_path)
        classes = Path(settings.yolo_classes_path)
        if not (cfg.exists() and weights.exists() and classes.exists()):
            raise FileNotFoundError("YOLOv2 config/weights/classes file missing. Use mock mode or add weights.")
        self.net = cv2.dnn.readNetFromDarknet(str(cfg), str(weights))
        self.layer_names = self.net.getUnconnectedOutLayersNames()
        self.classes = [line.strip() for line in classes.read_text().splitlines() if line.strip()]

    def detect(self, frame: np.ndarray) -> list[Detection]:
        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.layer_names)

        boxes, confidences, class_ids = [], [], []
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(np.argmax(scores))
                confidence = float(scores[class_id])
                if confidence < settings.confidence_threshold:
                    continue
                center_x, center_y, w, h = detection[:4]
                box_w, box_h = int(w * width), int(h * height)
                x = int(center_x * width - box_w / 2)
                y = int(center_y * height - box_h / 2)
                boxes.append([x, y, box_w, box_h])
                confidences.append(confidence)
                class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, settings.confidence_threshold, settings.nms_threshold)
        detections: list[Detection] = []
        if len(indices) > 0:
            for idx in indices.flatten():
                label = self.classes[class_ids[idx]] if class_ids[idx] < len(self.classes) else str(class_ids[idx])
                if label not in VEHICLE_CLASSES:
                    continue
                x, y, w, h = boxes[idx]
                detections.append(Detection(label=label, confidence=float(confidences[idx]), bbox=(x, y, w, h)))
        return detections


_detector: BaseDetector | None = None


def get_detector() -> BaseDetector:
    global _detector
    if _detector is None:
        _detector = MockDetector() if settings.detection_mode.lower() == "mock" else YOLOv2Detector()
    return _detector
