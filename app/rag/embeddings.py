"""Deterministic local embeddings for reliable demos and tests."""

from __future__ import annotations

import hashlib
import re

import numpy as np


TOKEN_RE = re.compile(r"[A-Za-z0-9_\u4e00-\u9fff]+")


class HashingEmbeddingModel:
    """Embed text with hashed lexical features.

    This keeps the GitHub demo runnable without API keys or model downloads.
    The class is intentionally small so it can be swapped for OpenAI,
    SentenceTransformers, FAISS, Chroma, or LlamaIndex embeddings.
    """

    def __init__(self, dim: int = 512):
        self.dim = dim

    def embed(self, text: str) -> np.ndarray:
        vector = np.zeros(self.dim, dtype=np.float32)
        for feature in self._features(text):
            digest = hashlib.md5(feature.encode("utf-8")).hexdigest()
            index = int(digest[:8], 16) % self.dim
            vector[index] += 1.0

        norm = float(np.linalg.norm(vector))
        if norm:
            vector /= norm
        return vector

    def _features(self, text: str) -> list[str]:
        tokens = [token.lower() for token in TOKEN_RE.findall(text)]
        bigrams = [f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)]
        return tokens + bigrams
