from fastapi import APIRouter
from pydantic import BaseModel

from app.ingestion.pipeline import process_video
from app.utils.platform_detector import detect_platform

router = APIRouter()


class VideoRequest(BaseModel):
    url: str
    comparison_label: str


@router.post("/video")
async def ingest_video(request: VideoRequest):

    if not request.url.strip():
        return {
            "error": "URL is required"
        }

    platform = detect_platform(
        request.url
    )

    if platform == "unknown":
        return {
            "error": "Unsupported platform"
        }

    result = process_video(
        request.url,
        platform,
        request.comparison_label
    )

    return result

