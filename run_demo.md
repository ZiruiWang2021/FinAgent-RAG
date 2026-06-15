# Run Demo

This guide walks through the FinAgent-RAG demo from a clean terminal.

## 1. Install

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

## 2. Start FastAPI

```bash
uvicorn app.main:app --reload --port 8000
```

Check:

```bash
curl http://localhost:8000/health
```

## 3. Start Streamlit

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

## 4. Demo Flow

1. Upload `data/sample_docs/demo_company.md`.
2. Ask: `What drives ACME revenue growth?`
3. Ask: `What are the key risks?`
4. Enter ticker `AAPL` and click `Analyze Stock`.
5. Click `Run Agent Workflow`.
6. Review retrieved sources, stock metrics, agent steps, and final report.

## 5. API-Only Demo

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@data/sample_docs/demo_company.md"
```

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What drives ACME revenue growth?","top_k":4}'
```

```bash
curl -X POST http://localhost:8000/generate-report \
  -H "Content-Type: application/json" \
  -d '{"question":"Summarize ACME growth drivers and risks.","ticker":"AAPL","top_k":4}'
```
