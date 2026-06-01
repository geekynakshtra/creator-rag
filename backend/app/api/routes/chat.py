import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.rag.memory_store import conversation_memory
from app.rag.response_generator import (
    generate_rag_response,
    stream_rag_response
)

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


def detect_query_mode(query: str) -> str:
    query_lower = query.lower()

    if (
        "hook" in query_lower
        or "first 5 seconds" in query_lower
        or "intro" in query_lower
    ):
        return "hook_analysis"

    if (
        "engagement" in query_lower
        or "viral" in query_lower
        or "perform" in query_lower
        or "views" in query_lower
    ):
        return "engagement_analysis"

    if (
        "improve" in query_lower
        or "suggest" in query_lower
        or "better" in query_lower
    ):
        return "improvement_analysis"

    if (
        "creator" in query_lower
        or "who made" in query_lower
        or "channel" in query_lower
        or "follower" in query_lower
    ):
        return "creator_analysis"

    return "general_analysis"


def get_memory_context() -> str:
    return "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in conversation_memory[-6:]
    ])


@router.post("/")
async def chat(request: ChatRequest):
    memory_context = get_memory_context()
    mode = detect_query_mode(request.query)

    response = generate_rag_response(
        request.query,
        memory_context,
        mode
    )

    conversation_memory.append({
        "role": "user",
        "content": request.query
    })

    conversation_memory.append({
        "role": "assistant",
        "content": response["answer"]
    })

    return response


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    memory_context = get_memory_context()
    mode = detect_query_mode(request.query)

    async def event_generator():
        full_answer = ""

        async for chunk in stream_rag_response(
            request.query,
            memory_context,
            mode
        ):
            if chunk.get("type") == "token":
                full_answer += chunk["content"]

            yield f"data: {json.dumps(chunk)}\n\n"

        conversation_memory.append({
            "role": "user",
            "content": request.query
        })

        conversation_memory.append({
            "role": "assistant",
            "content": full_answer
        })

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )