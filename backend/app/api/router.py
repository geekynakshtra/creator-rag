from fastapi import APIRouter

from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.chat import (router as chat_router)
api_router = APIRouter()

api_router.include_router(
    ingestion_router,
    prefix="/ingest",
    tags=["Ingestion"])

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"])