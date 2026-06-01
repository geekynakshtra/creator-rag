from pydantic import BaseModel
from typing import Optional


class VideoMetadata(BaseModel):
    video_id: str
    platform: str
    title: str
    creator: str
    views: int
    likes: int
    comments: int
    duration: int
    upload_date: Optional[str] = None
    hashtags: list[str] = []
    transcript: str
    engagement_rate: float