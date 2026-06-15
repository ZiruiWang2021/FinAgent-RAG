"""Application container and dependency wiring."""

from __future__ import annotations

from dataclasses import dataclass

from app.agents.workflow import AgentWorkflow
from app.config import settings
from app.rag.embeddings import HashingEmbeddingModel
from app.rag.retriever import DocumentIndexer, RagRetriever, RagService
from app.rag.vector_store import InMemoryVectorStore
from app.tools.stock_data_tool import StockDataTool


@dataclass
class AppContainer:
    vector_store: InMemoryVectorStore
    document_indexer: DocumentIndexer
    rag_service: RagService
    stock_tool: StockDataTool
    workflow: AgentWorkflow


def create_container() -> AppContainer:
    vector_store = InMemoryVectorStore(HashingEmbeddingModel(dim=settings.embedding_dim))
    document_indexer = DocumentIndexer(
        vector_store=vector_store,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    rag_service = RagService(RagRetriever(vector_store))
    stock_tool = StockDataTool()
    workflow = AgentWorkflow(rag_service=rag_service, stock_tool=stock_tool)
    return AppContainer(
        vector_store=vector_store,
        document_indexer=document_indexer,
        rag_service=rag_service,
        stock_tool=stock_tool,
        workflow=workflow,
    )
