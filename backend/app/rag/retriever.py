from app.services.embedding_service import (generate_embedding)

from app.services.vector_db_service import (collection)


def retrieve_relevant_chunks(
    query: str,
    limit: int = 5,
    mode: str = "general_analysis"
):


# GENERATE QUERY EMBEDDING
    query_embedding = generate_embedding(query)

# MODE-BASED FILTERING
    where_filter = None

    if mode == "hook_analysis":
        where_filter = {
            "chunk_index": 0
        }

    if mode == "improvement_analysis":
        where_filter = {
            "chunk_index": 0
        }

# QUERY VECTOR DB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
        where=where_filter
    )

    formatted_results = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

# FORMAT RESULTS
    for doc, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        score = 1 - distance


        formatted_results.append({

            "score": score,

            "text": doc,

            "video_id": metadata.get("video_id"),

            "title": metadata.get("title"),

            "creator": metadata.get("creator"),

            "chunk_index": metadata.get("chunk_index"),

            "platform": metadata.get("platform"),

            "comparison_label": metadata.get("comparison_label"),

            "views": metadata.get("views"),

            "likes": metadata.get("likes"),

            "comments": metadata.get("comments"),

            "engagement_rate": metadata.get("engagement_rate"),

            "follower_count": metadata.get("follower_count"),

            "duration": metadata.get("duration"),

            "context": f"""
VIDEO {metadata.get("comparison_label")}

TITLE:
{metadata.get("title")}

CREATOR:
{metadata.get("creator")}

PLATFORM:
{metadata.get("platform")}

VIEWS:
{metadata.get("views")}

LIKES:
{metadata.get("likes")}

COMMENTS:
{metadata.get("comments")}

ENGAGEMENT RATE:
{metadata.get("engagement_rate")}%

"follower_count":
{metadata.get("follower_count")}
    
DURATION:
{metadata.get("duration")} seconds

CHUNK INDEX:
{metadata.get("chunk_index")}

TRANSCRIPT:
{doc}
"""
        })
    return formatted_results