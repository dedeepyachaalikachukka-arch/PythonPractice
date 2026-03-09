from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import boto3
import cv2
import numpy as np

from app.core.config import settings


class EvidenceStorage:
    def __init__(self) -> None:
        self.local_dir = Path("data/evidence")
        self.local_dir.mkdir(parents=True, exist_ok=True)

        self.use_s3 = bool(settings.s3_bucket_name and settings.aws_access_key_id and settings.aws_secret_access_key)
        self.client = None
        if self.use_s3:
            self.client = boto3.client(
                "s3",
                region_name=settings.aws_region,
                endpoint_url=settings.s3_endpoint_url or None,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
            )

    def save_frame(self, frame: np.ndarray, camera_id: int) -> str:
        filename = f"camera_{camera_id}_{uuid4().hex}.jpg"
        local_path = self.local_dir / filename
        cv2.imwrite(str(local_path), frame)
        if self.client:
            self.client.upload_file(str(local_path), settings.s3_bucket_name, filename)
            return f"s3://{settings.s3_bucket_name}/{filename}"
        return str(local_path)
