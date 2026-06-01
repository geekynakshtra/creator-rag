from app.ingestion.transcript_service import (extract_video_data)

from app.ingestion.chunking import (chunk_transcript)

from app.services.embedding_service import (generate_embedding)

from app.services.vector_db_service import (collection)


def process_video(
    url: str,
    platform: str,
    comparison_label: str
):

    video_data = extract_video_data(
        url,
        platform
    )

    video_data["comparison_label"] = comparison_label

    print("INGESTING VIDEO:",video_data.get("title"))

    print("COMPARISON LABEL:",comparison_label)

    transcript = (
        video_data.get("transcript")
        or ""
    )

    if not transcript.strip():

        video_data["transcript_warning"] = True

        transcript = (
            f"{video_data.get('title', '')} "
            f"{video_data.get('creator', '')}"
        )

    views = (
        video_data.get("views")
        or 0
    )

    likes = (
        video_data.get("likes")
        or 0
    )

    comments = (
        video_data.get("comments")
        or 0
    )

    if (
        platform == "instagram"
        and views == 0
        and likes > 0
    ):

        estimated_views = likes * 20

        views = estimated_views

        video_data["views"] = estimated_views

        video_data["estimated_views"] = True

    if views > 0:

        engagement_rate = (
            (likes + comments) / views
        ) * 100

    else:

        engagement_rate = 0

    video_data["engagement_rate"] = round(
        engagement_rate,
        2
    )

    video_data["views"] = views
    video_data["likes"] = likes
    video_data["comments"] = comments

    if views == 0:
        video_data["data_quality_warning"] = True

    chunks = chunk_transcript(
        transcript
    )

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(
            chunk
        )

        collection.add(
            ids=[
                f"{comparison_label}_{video_data['video_id']}_{index}"
            ],
            documents=[
                chunk
            ],
            embeddings=[
                embedding
            ],
            metadatas=[{
                "video_id": str(video_data.get("video_id")),
                "comparison_label": str(comparison_label),
                "title": str(video_data.get("title", "")),
                "creator": str(video_data.get("creator", "")),
                "platform": str(platform),
                "chunk_index": int(index),
                "views": int(video_data.get("views", 0)),
                "likes": int(video_data.get("likes", 0)),
                "comments": int(video_data.get("comments", 0)),
                "follower_count": int(video_data.get("follower_count") or 0),
                "engagement_rate": float(video_data.get("engagement_rate", 0)),
                "duration": float(video_data.get("duration", 0))
            }]
        )

    return video_data