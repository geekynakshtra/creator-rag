import os
import uuid
import yt_dlp
import whisper


whisper_model = whisper.load_model("base")


def transcribe_video_audio(url: str) -> str:

    os.makedirs(
        "temp_audio",
        exist_ok=True
    )

    file_id = str(uuid.uuid4())

    output_template = (
        f"temp_audio/{file_id}.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    downloaded_audio_path = (
        f"temp_audio/{file_id}.mp3"
    )

    try:

        with yt_dlp.YoutubeDL(
            ydl_opts
        ) as ydl:

            ydl.download([url])

        result = whisper_model.transcribe(
            downloaded_audio_path
        )

        transcript = (
            result.get("text") or ""
        )

        return transcript.strip()

    finally:

        if os.path.exists(
            downloaded_audio_path
        ):

            os.remove(
                downloaded_audio_path
            )