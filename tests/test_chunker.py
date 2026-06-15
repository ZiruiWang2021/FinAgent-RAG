from app.rag.chunker import chunk_text


def test_chunk_text_creates_overlapping_chunks():
    text = " ".join([f"Revenue growth driver sentence {index}." for index in range(80)])

    chunks = chunk_text(text, source="sample.md", chunk_size=180, overlap=40)

    assert len(chunks) > 1
    assert chunks[0].source == "sample.md"
    assert chunks[0].chunk_id == "sample.md#0"
    assert chunks[1].char_start < chunks[0].char_end
    assert all(chunk.content for chunk in chunks)


def test_chunk_text_rejects_invalid_overlap():
    try:
        chunk_text("hello", source="x.txt", chunk_size=100, overlap=100)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
