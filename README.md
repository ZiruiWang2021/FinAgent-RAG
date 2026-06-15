# FinAgent-RAG

FinAgent-RAG is a production-oriented AI Agent demo for financial research reports, company announcements, and stock market data. It is designed to showcase multi-agent workflow design, retrieval-augmented generation, tool calling, FastAPI backend engineering, Streamlit demo UX, and testable project structure.

> This project is for engineering demonstration and research workflow prototyping only. It is not investment advice.

## Why This Project Fits an AI Agent Engineer Role

- Multi-agent workflow for task planning, retrieval, data analysis, risk reasoning, and report generation
- RAG pipeline over financial documents with source-grounded answers
- Tool calling for real stock data analysis through `yfinance`
- FastAPI backend with modular API router design
- Streamlit demo interface for end-to-end interaction
- Evaluation examples and tests to reduce hallucination and check retrieval quality
- Clean project structure suitable for extension into enterprise AI applications

## Tech Stack

- Python
- FastAPI
- Streamlit
- Pydantic
- pandas / numpy
- yfinance
- pypdf
- pytest

The current retriever uses deterministic hashing embeddings so the project runs without API keys or model downloads. In production, the `app/rag/` boundary can be replaced with OpenAI embeddings, SentenceTransformers, FAISS, Chroma, pgvector, LangChain, or LlamaIndex.

## Suggested Repo Structure

```text
finagent-rag/
|-- app/
|   |-- main.py
|   |-- api/
|   |   |-- upload.py
|   |   |-- ask.py
|   |   |-- stock.py
|   |   `-- report.py
|   |-- agents/
|   |   |-- planner_agent.py
|   |   |-- retriever_agent.py
|   |   |-- data_agent.py
|   |   |-- risk_agent.py
|   |   |-- report_agent.py
|   |   `-- workflow.py
|   |-- rag/
|   |   |-- document_loader.py
|   |   |-- chunker.py
|   |   |-- embeddings.py
|   |   |-- vector_store.py
|   |   `-- retriever.py
|   |-- tools/
|   |   |-- stock_data_tool.py
|   |   |-- financial_metrics.py
|   |   `-- chart_tool.py
|   |-- prompts/
|   |   |-- planner_prompt.txt
|   |   |-- rag_prompt.txt
|   |   |-- risk_prompt.txt
|   |   `-- report_prompt.txt
|   `-- schemas/
|       `-- models.py
|-- frontend/
|   `-- streamlit_app.py
|-- data/
|   |-- sample_docs/
|   `-- vector_store/
|-- tests/
|   |-- test_chunker.py
|   |-- test_stock_tool.py
|   |-- test_retriever.py
|   `-- test_api.py
|-- README.md
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- run_demo.md
```

## Architecture

```text
User
  |
  | Streamlit frontend
  v
FastAPI backend
  |
  +-- POST /upload
  |     document_loader -> chunker -> embeddings -> vector_store
  |
  +-- POST /ask
  |     retriever -> source-grounded RAG answer
  |
  +-- POST /analyze-stock
  |     stock_data_tool -> financial_metrics
  |
  +-- POST /generate-report
        Planner Agent
          -> Retriever Agent
          -> Data Agent
          -> Risk Agent
          -> Report Agent
```

## Core Features

1. Upload `txt`, `md`, and `pdf` documents.
2. Extract text, chunk documents, embed chunks, and retrieve relevant passages.
3. Answer company, industry, risk, business model, and financial performance questions with citations.
4. Analyze stock market data with 1-month return, annualized volatility, MA20, MA60, maximum drawdown, and trend.
5. Run a simple multi-agent workflow that exposes each intermediate step.
6. Use a Streamlit frontend for upload, question answering, ticker analysis, workflow tracing, and final report generation.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the Backend

```bash
uvicorn app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

## Run the Frontend

In a second terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open the Streamlit URL shown in the terminal, usually `http://localhost:8501`.

## API Examples

Upload a document:

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@data/sample_docs/demo_company.md"
```

Ask a RAG question:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What are ACME growth drivers and risks?","top_k":4}'
```

Analyze a stock:

```bash
curl -X POST http://localhost:8000/analyze-stock \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","period":"6mo"}'
```

Generate a multi-agent report:

```bash
curl -X POST http://localhost:8000/generate-report \
  -H "Content-Type: application/json" \
  -d '{"question":"Analyze ACME business drivers, financial performance, and key risks.","ticker":"AAPL","top_k":4}'
```

## Demo Questions

- What are the main revenue growth drivers?
- What risks does the company disclose?
- How does the company describe its business model?
- What financial performance trend is mentioned in the report?
- What industry headwinds or regulatory risks should investors monitor?
- Generate a structured report and include market data for `AAPL`.

## Evaluation Examples

Use `data/sample_docs/demo_company.md` as a small controlled document set:

- Ask: `What drives ACME revenue growth?`
  - Expected evidence should mention cloud software subscriptions and enterprise customer expansion.
- Ask: `What are ACME's main risks?`
  - Expected evidence should mention competition, customer concentration, sales cycle uncertainty, or margin pressure.
- Ask: `What is ACME's dividend policy?`
  - Expected behavior should be cautious because the sample document does not contain this information.

## Tests

```bash
pytest
```

The test suite covers:

- document chunking
- retrieval relevance
- stock indicator calculations
- FastAPI upload, RAG answer, stock analysis, and report generation

## Extension Ideas

- Replace local hashing embeddings with OpenAI embeddings plus FAISS or Chroma.
- Add persistent document collections and metadata filters by company, date, sector, and document type.
- Use LangGraph or CrewAI for richer multi-agent planning, retries, and state transitions.
- Add SEC filing ingestion, earnings transcript parsing, and scheduled market data refresh.
- Add structured evaluation datasets for retrieval quality, citation coverage, and hallucination detection.
- Add authentication, rate limiting, background jobs, observability, and deployment manifests.
