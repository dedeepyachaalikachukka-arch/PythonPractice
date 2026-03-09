from pydantic import BaseModel, Field


class CameraCreate(BaseModel):
    name: str
    location: str
    source_url: str
    stop_line_y: int | None = None
    red_light_roi: list[int] | None = Field(default=None, description="[x1,y1,x2,y2]")


class CameraRead(CameraCreate):
    id: int

    model_config = {"from_attributes": True}
