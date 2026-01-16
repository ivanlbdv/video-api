from datetime import datetime, timedelta

import isodate
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
    def duration_positive(cls, v: str | timedelta) -> timedelta:
        if isinstance(v, timedelta):
            if v <= timedelta(0):
                raise ValueError('duration must be positive')
            return v

        try:
            td = isodate.parse_duration(v)
            if td <= timedelta(0):
                raise ValueError('duration must be positive')
            return td
        except isodate.ISO8601Error:
            raise ValueError(
                'Invalid ISO 8601 duration format (e.g., "PT1H", "PT30M")'
            )

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
