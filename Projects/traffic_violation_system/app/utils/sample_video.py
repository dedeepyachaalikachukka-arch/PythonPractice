from pathlib import Path

import cv2
import numpy as np


def create_sample_video(path: str = "sample.mp4", frames: int = 30) -> str:
    output = Path(path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(output), fourcc, 10.0, (640, 480))
    for i in range(frames):
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, f"Frame {i+1}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.rectangle(frame, (150 + i * 2, 240), (320 + i * 2, 360), (0, 255, 0), 3)
        cv2.line(frame, (0, 340), (639, 340), (0, 0, 255), 2)
        writer.write(frame)
    writer.release()
    return str(output)


if __name__ == "__main__":
    print(create_sample_video())
