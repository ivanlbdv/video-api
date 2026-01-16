from datetime import datetime, timedelta

from pydantic import BaseModel, field_validator


class VideoBase(BaseModel):
    video_path: str
    start_time: datetime
    duration: timedelta
    camera_number: int
    location: str


class VideoCreate(VideoBase):
    @field_validator('video_path')
    @classmethod
    def video_path_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('video_path cannot be empty')
        return v

    @field_validator('duration')
    @classmethod
    def duration_positive(cls, v: timedelta) -> timedelta:
        if v <= timedelta(0):
            raise ValueError('duration must be positive')
        return v

    @field_validator('camera_number')
    @classmethod
    def camera_number_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('camera_number must be positive')
        return v

    @field_validator('location')
    @classmethod
    def location_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('location cannot be empty')
        return v


class VideoUpdateStatus(BaseModel):
    status: str

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        valid_statuses = ['new', 'transcoded', 'recognized']
        if v not in valid_statuses:
            raise ValueError(f'status must be one of: {valid_statuses}')
        return v


class VideoResponse(VideoBase):
    id: int
    status: str
    created_at: datetime

    model_config = {'from_attributes': True}
