import yt_dlp


def extract_youtube_metadata(url: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "video_id": info.get("id"),
        "title": info.get("title"),
        "creator": info.get("uploader"),
        "views": info.get("view_count", 0),
        "likes": info.get("like_count", 0),
        "comments": info.get("comment_count", 0),
        "duration": info.get("duration", 0),
        "upload_date": info.get("upload_date"),
        "hashtags": info.get("tags", [])
    }