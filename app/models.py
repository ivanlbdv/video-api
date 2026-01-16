from datetime import datetime, timezone

from app.database import Base
from sqlalchemy import Column, DateTime, Integer, Interval, String


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    video_path = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Interval, nullable=False)
    camera_number = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, default='new')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
