def detect_platform(url: str):

    url = url.lower()

    if (
        "youtube.com" in url or
        "youtu.be" in url
    ):
        return "youtube"

    if "instagram.com" in url:
        return "instagram"

    return "unknown"