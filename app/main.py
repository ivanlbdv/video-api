from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

from app import database, models, schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI(title='Video API', version='1.0.0')


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.Base.metadata.create_all(bind=database.engine)
    yield

setattr(app, 'lifespan', lifespan)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/videos', response_model=schemas.VideoResponse, status_code=201)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    db_video = models.Video(**video.model_dump())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


@app.get('/videos', response_model=List[schemas.VideoResponse])
def get_videos(
    status: Optional[List[str]] = None,
    camera_number: Optional[List[int]] = None,
    location: Optional[List[str]] = None,
    start_time_from: Optional[datetime] = None,
    start_time_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Video)

    if status:
        query = query.filter(models.Video.status.in_(status))
    if camera_number:
        query = query.filter(models.Video.camera_number.in_(camera_number))
    if location:
        query = query.filter(models.Video.location.in_(location))
    if start_time_from:
        query = query.filter(models.Video.start_time >= start_time_from)
    if start_time_to:
        query = query.filter(models.Video.start_time <= start_time_to)

    return query.all()


@app.get('/videos/{video_id}', response_model=schemas.VideoResponse)
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')
    return video


@app.patch('/videos/{video_id}/status', response_model=schemas.VideoResponse)
def update_video_status(
    video_id: int,
    status_update: schemas.VideoUpdateStatus,
    db: Session = Depends(get_db),
):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail='Video not found')

    valid_statuses = ['new', 'transcoded', 'recognized']
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid status. Must be one of: {valid_statuses}',
        )

    video.status = status_update.status
    db.commit()
    db.refresh(video)
    return video
