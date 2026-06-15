from app.rag.chunker import chunk_text
from app.rag.vector_store import InMemoryVectorStore


def test_vector_store_returns_relevant_chunk():
    store = InMemoryVectorStore()
    chunks = []
    chunks.extend(
        chunk_text(
            "ACME revenue grew because cloud software subscriptions expanded across enterprise customers.",
            source="acme.md",
            chunk_size=300,
            overlap=20,
        )
    )
    chunks.extend(
        chunk_text(
            "Beta Bank faces liquidity risk and higher credit losses in a downturn.",
            source="beta.md",
            chunk_size=300,
            overlap=20,
        )
    )
    store.add_chunks(chunks)

    results = store.search("What drove ACME revenue growth?", top_k=1)

    assert len(results) == 1
    assert results[0].source == "acme.md"
    assert "cloud software" in results[0].content
