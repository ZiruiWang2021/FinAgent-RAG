import pandas as pd
from fastapi.testclient import TestClient

from app.main import create_app


def test_upload_and_ask_api_returns_sources():
    app = create_app()
    client = TestClient(app)

    upload = client.post(
        "/upload",
        files={
            "file": (
                "acme.md",
                b"ACME revenue growth came from cloud subscriptions. Competition is the key risk.",
                "text/markdown",
            )
        },
    )
    assert upload.status_code == 200
    assert upload.json()["chunks_indexed"] >= 1

    ask = client.post("/ask", json={"question": "What drove ACME revenue growth?", "top_k": 2})
    assert ask.status_code == 200
    body = ask.json()
    assert body["sources"]
    assert "cloud subscriptions" in body["answer"]


def test_analyze_stock_api_uses_injected_tool_boundary():
    app = create_app()
    client = TestClient(app)

    def fake_fetch_history(ticker: str, period: str = "6mo"):
        dates = pd.date_range("2024-01-01", periods=80, freq="B")
        return pd.DataFrame({"Close": [100 + index for index in range(80)]}, index=dates)

    app.state.container.stock_tool.fetch_history = fake_fetch_history

    response = client.post("/analyze-stock", json={"ticker": "MOCK", "period": "6mo"})

    assert response.status_code == 200
    body = response.json()
    assert body["metrics"]["ticker"] == "MOCK"
    assert body["metrics"]["trend"].startswith("Bullish")


def test_generate_report_api_returns_agent_steps():
    app = create_app()
    client = TestClient(app)

    client.post(
        "/upload",
        files={
            "file": (
                "risk.md",
                b"ACME has strong recurring revenue. The main risk is customer concentration.",
                "text/markdown",
            )
        },
    )

    response = client.post(
        "/generate-report",
        json={"question": "What are ACME risks?", "top_k": 2},
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body["steps"]) >= 4
    assert "FinAgent-RAG Analysis Report" in body["report"]
    assert body["tool_calls"]
    assert body["structured_report"]["citations"]


def test_documents_and_evaluation_api():
    app = create_app()
    client = TestClient(app)

    client.post(
        "/upload",
        files={
            "file": (
                "demo_company.md",
                (
                    b"ACME revenue growth is driven by cloud software subscriptions and enterprise customer expansion. "
                    b"The company benefits from recurring revenue, high renewal rates, and operating leverage. "
                    b"Key risks include competition, customer concentration, sales cycle uncertainty, and margin pressure from infrastructure costs."
                ),
                "text/markdown",
            )
        },
    )

    documents = client.get("/documents")
    assert documents.status_code == 200
    assert documents.json()["total_chunks"] >= 1

    cases = client.get("/evaluation-cases")
    assert cases.status_code == 200
    assert len(cases.json()) >= 5

    evaluation = client.post("/evaluate")
    assert evaluation.status_code == 200
    body = evaluation.json()
    assert body["total_cases"] >= 5
    assert "average_groundedness_score" in body
