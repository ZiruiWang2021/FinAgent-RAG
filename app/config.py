"""Application configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
SAMPLE_DOCS_DIR = DATA_DIR / "sample_docs"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"


@dataclass(frozen=True)
class Settings:
    app_name: str = "FinAgent-RAG"
    chunk_size: int = int(os.getenv("FINAGENT_CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("FINAGENT_CHUNK_OVERLAP", "120"))
    embedding_dim: int = int(os.getenv("FINAGENT_EMBEDDING_DIM", "512"))
    default_top_k: int = int(os.getenv("FINAGENT_DEFAULT_TOP_K", "4"))
    upload_dir: Path = UPLOAD_DIR


settings = Settings()


def ensure_data_dirs() -> None:
    for directory in [DATA_DIR, UPLOAD_DIR, SAMPLE_DOCS_DIR, VECTOR_STORE_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
