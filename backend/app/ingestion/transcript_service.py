import re
import yt_dlp

from youtube_transcript_api import (YouTubeTranscriptApi)

from app.ingestion.whisper_service import (transcribe_video_audio)


def extract_hashtags(text: str):
    if not text:
        return []

    hashtags = re.findall(
        r"#\w+",
        text
    )

    return list(dict.fromkeys([
        tag.replace("#", "")
        for tag in hashtags
    ]))


def extract_youtube_transcript(
    video_id: str
):
    try:
        transcript_data = (
            YouTubeTranscriptApi.get_transcript(
                video_id
            )
        )

        transcript = " ".join([
            item["text"]
            for item in transcript_data
        ])

        return transcript

    except Exception:
        return ""


def extract_video_data(
    url: str,
    platform: str = "youtube"
):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": False
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:
        info = ydl.extract_info(
            url,
            download=False
        )

    video_id = info.get("id")

    title = (
        info.get("title")
        or ""
    )

    description = (
        info.get("description")
        or ""
    )

    yt_tags = (
        info.get("tags")
        or []
    )

    caption_hashtags = extract_hashtags(
        f"{title} {description}"
    )

    hashtags = (
        yt_tags
        if yt_tags
        else caption_hashtags
    )

    transcript = ""

    if platform == "youtube":

        transcript = extract_youtube_transcript(
            video_id
        )

        if not transcript.strip():
            transcript = description

    elif platform == "instagram":

        transcript = transcribe_video_audio(
            url
        )

        if not transcript.strip():
            transcript = description

    else:
        transcript = description

    follower_count = (
        info.get("channel_follower_count")
        or info.get("uploader_follower_count")
        or 0
    )

    return {
        "video_id": video_id,
        "title": title,
        "creator": info.get("uploader"),
        "views": info.get("view_count") or 0,
        "likes": info.get("like_count") or 0,
        "comments": info.get("comment_count") or 0,
        "duration": info.get("duration") or 0,
        "upload_date": info.get("upload_date"),
        "hashtags": hashtags,
        "transcript": transcript,
        "follower_count": follower_count,
    }