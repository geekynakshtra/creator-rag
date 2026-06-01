from app.rag.retriever import (retrieve_relevant_chunks)

from app.rag.prompts import (build_rag_prompt)

from app.services.llm_service import (llm)


def generate_rag_response(
    query,
    memory_context="",
    mode="general_analysis"
):


# RETRIEVE RELEVANT CHUNKS
    chunks = retrieve_relevant_chunks(
        query,
        mode=mode
    )


# BUILD METADATA SUMMARY
    metadata_summary = ""

    seen_videos = set()

    for chunk in chunks:

        video_id = chunk.get(
            "video_id"
        )

        # Prevent duplicate metadata
        if video_id in seen_videos:
            continue

        seen_videos.add(video_id)

        metadata_summary += f"""

VIDEO {chunk.get('comparison_label')}

TITLE:
{chunk.get('title')}

CREATOR:
{chunk.get('creator')}

PLATFORM:
{chunk.get('platform')}

VIEWS:
{chunk.get('views')}

LIKES:
{chunk.get('likes')}

COMMENTS:
{chunk.get('comments')}

ENGAGEMENT RATE:
{chunk.get('engagement_rate')}%

DURATION:
{chunk.get('duration')} seconds

FOLLOWERS:
{chunk.get('follower_count')}

"""
    print(metadata_summary)

# BUILD PROMPT
    prompt = build_rag_prompt(
        query,
        chunks,
        memory_context,
        mode,
        metadata_summary
    )

# GENERATE RESPONSE
    answer = llm.invoke(
        prompt
    )


# CLEAN OUTPUT
    if hasattr(answer, "content"):

        answer_text = answer.content

    else:

        answer_text = str(answer)


# FINAL RESPONSE
    return {

        "query": query,

        "answer": answer_text,

        "sources": chunks
    }

async def stream_rag_response(
    query,
    memory_context="",
    mode="general_analysis"
):

    chunks = retrieve_relevant_chunks(
        query,
        mode=mode
    )


    metadata_summary = ""

    seen_videos = set()

    for chunk in chunks:
        video_id = chunk.get("video_id")

        if video_id in seen_videos:
            continue

        seen_videos.add(video_id)

        metadata_summary += f"""

VIDEO {chunk.get('comparison_label')}

TITLE:
{chunk.get('title')}

CREATOR:
{chunk.get('creator')}

PLATFORM:
{chunk.get('platform')}

VIEWS:
{chunk.get('views')}

LIKES:
{chunk.get('likes')}

COMMENTS:
{chunk.get('comments')}

ENGAGEMENT RATE:
{chunk.get('engagement_rate')}%

FOLLOWERS:
{chunk.get('follower_count')}

DURATION:
{chunk.get('duration')} seconds

"""

    prompt = build_rag_prompt(
        query,
        chunks,
        memory_context,
        mode,
        metadata_summary
    )


    yield {
        "type": "sources",
        "content": chunks
    }


    for token in llm.stream(prompt):

        if hasattr(token, "content"):
            token_text = token.content
        else:
            token_text = str(token)



        if token_text:
            yield {
                "type": "token",
                "content": token_text
            }
