from sqlalchemy import JSON, Column, Integer, String

from app.db.base import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    stop_line_y = Column(Integer, nullable=True)
    red_light_roi = Column(JSON, nullable=True)
