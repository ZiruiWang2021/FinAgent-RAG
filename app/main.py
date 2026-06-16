"""FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ask, documents, evaluation, report, stock, upload
from app.config import ensure_data_dirs, settings
from app.dependencies import create_container


def create_app() -> FastAPI:
    ensure_data_dirs()
    api = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="A multi-agent RAG system for financial documents and stock data.",
    )
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api.state.container = create_container()

    @api.get("/health")
    def health() -> dict[str, str | int]:
        return {
            "status": "ok",
            "indexed_chunks": len(api.state.container.vector_store),
        }

    api.include_router(upload.router)
    api.include_router(documents.router)
    api.include_router(ask.router)
    api.include_router(stock.router)
    api.include_router(report.router)
    api.include_router(evaluation.router)
    return api


app = create_app()
