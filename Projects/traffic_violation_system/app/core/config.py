from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Smart Traffic Violation Detection System"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    database_url: str = "sqlite:///./traffic.db"
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "traffic-violation-evidence"
    s3_endpoint_url: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    detection_mode: str = "mock"
    yolo_config_path: str = "weights/yolov2.cfg"
    yolo_weights_path: str = "weights/yolov2.weights"
    yolo_classes_path: str = "weights/coco.names"
    confidence_threshold: float = 0.45
    nms_threshold: float = 0.40
    frame_sample_rate: int = 10

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
