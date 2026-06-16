# FinAgent-RAG

FinAgent-RAG is an AI Native financial information and research workflow. It combines RAG, agent orchestration, prompt templates, tool calling, structured output validation, and evaluation checks in a compact full-stack project.

FinAgent-RAG 是一个 AI Native 金融资讯与研究分析系统。项目将 RAG、多 Agent 工作流、Prompt Engineering、工具调用、结构化输出校验和模型评估整合在一个简洁的全栈工程中。

> This repository is a research workflow prototype. It is not investment advice.  
> 本仓库用于研究流程原型验证，不构成任何投资建议。

## Positioning / 项目定位

The system targets financial document Q&A and market-data-assisted research. Users can upload reports or announcements, ask source-grounded questions, inspect citations, run an agent workflow, review tool calls, generate a structured report, and run simple evaluation cases.

系统面向金融文档问答和股票数据辅助研究。用户可以上传研报或公告，进行带引用来源的问答，查看 Agent 执行步骤和工具调用记录，生成结构化报告，并运行简单评估集检查回答质量。

## Architecture / 架构

```text
React + TypeScript UI
  |-- document upload
  |-- RAG Q&A
  |-- citations
  |-- agent steps
  |-- tool calls
  |-- structured report JSON
  `-- evaluation panel

FastAPI backend
  |-- /upload
  |-- /documents
  |-- /ask
  |-- /analyze-stock
  |-- /generate-report
  |-- /evaluation-cases
  `-- /evaluate

Core modules
  |-- RAG: document_loader -> chunker -> embeddings -> vector_store -> retriever
  |-- Agents: Planner -> Retriever -> Data -> Risk -> Report
  |-- Tools: stock data tool, financial metrics, chart data helper
  |-- Schemas: Pydantic validation for API and structured report output
  `-- Evaluation: expected answer points, source coverage, groundedness score
```

## Features / 功能

- Upload `txt`, `md`, and `pdf` documents.  
  支持上传 `txt`、`md` 和 `pdf` 文档。
- Run RAG Q&A with citations and retrieval scores.  
  支持带引用来源和检索分数的 RAG 问答。
- Generate a multi-agent report with observable workflow steps.  
  支持生成包含 Agent 步骤的多 Agent 分析报告。
- Record tool calls, including document retrieval and stock data analysis.  
  记录工具调用，包括文档检索和股票数据分析。
- Validate structured output using Pydantic schemas.  
  使用 Pydantic schema 校验结构化输出。
- Evaluate answer quality using at least 5 controlled test questions.  
  使用至少 5 个测试问题和期望答案要点评估回答质量。
- Apply basic hallucination control through source thresholds, citations, and unknown-answer evaluation.  
  通过相关性阈值、引用来源和未知问题评估进行基础 hallucination 控制。

## Tech Stack / 技术栈

- Backend: Python, FastAPI, Pydantic
- RAG: local hashing embeddings, in-memory vector store
- Agents: lightweight Planner / Retriever / Data / Risk / Report workflow
- Tools: yfinance, pandas, numpy
- Frontend: React, TypeScript, Vite
- Demo UI: Streamlit retained as a secondary lightweight interface
- Testing: pytest, FastAPI TestClient

## Repo Structure / 项目结构

```text
finagent-rag/
|-- app/
|   |-- api/
|   |-- agents/
|   |-- evaluation/
|   |-- prompts/
|   |-- rag/
|   |-- schemas/
|   |-- tools/
|   |-- dependencies.py
|   `-- main.py
|-- frontend-react/
|   |-- src/
|   |-- package.json
|   `-- vite.config.ts
|-- frontend/
|   `-- streamlit_app.py
|-- data/
|   |-- sample_docs/
|   |-- uploads/
|   `-- vector_store/
|-- tests/
|-- requirements.txt
|-- run_demo.md
`-- README.md
```

## API / 接口

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health and indexed chunk count |
| `POST` | `/upload` | Upload and index txt/md/pdf documents |
| `GET` | `/documents` | List indexed documents and chunk counts |
| `POST` | `/ask` | RAG Q&A with citations |
| `POST` | `/analyze-stock` | Stock metrics via yfinance |
| `POST` | `/generate-report` | Agent workflow, tool calls, structured report |
| `GET` | `/evaluation-cases` | Built-in evaluation questions |
| `POST` | `/evaluate` | Run evaluation against the current document index |

## Structured Output / 结构化输出

`/generate-report` returns both markdown text and validated JSON:

- `steps`: agent workflow trace
- `tool_calls`: tool name, input, status, output summary
- `sources`: retrieved chunks
- `structured_report`: title, executive summary, findings, risks, citations, stock metrics, hallucination controls

`/generate-report` 同时返回 markdown 报告和结构化 JSON，便于前端展示、自动评估和后续系统集成。

## Evaluation / 评估

The evaluation module contains 5 built-in cases:

1. Growth drivers
2. Business quality
3. Risk factors
4. Cost or margin pressure
5. Unknown dividend policy for hallucination control

评估模块会检查：

- expected answer point matching / 期望答案要点命中
- source count / 引用来源数量
- groundedness score / 基于来源的回答分数
- unknown-answer behavior / 未知问题拒答能力

## Run Backend / 启动后端

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run React Frontend / 启动 React 前端

Requires Node.js `>=20.19.0` because the React app uses Vite 7.

React 前端使用 Vite 7，建议 Node.js 版本 `>=20.19.0`。

```bash
cd frontend-react
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

打开 `http://127.0.0.1:5173`。

## Run Streamlit Demo / 启动 Streamlit Demo

```bash
streamlit run frontend/streamlit_app.py
```

## Demo Flow / 演示流程

1. Start FastAPI backend.  
   启动 FastAPI 后端。
2. Start React frontend.  
   启动 React 前端。
3. Upload `data/sample_docs/demo_company.md`.  
   上传样例文档。
4. Ask: `What drives ACME revenue growth?`  
   提问：`ACME 的收入增长由什么驱动？`
5. Generate an agent report with ticker `AAPL`.  
   使用 `AAPL` 生成 Agent 报告。
6. Review citations, agent steps, tool calls, and structured report JSON.  
   查看引用来源、Agent 步骤、工具调用和结构化报告 JSON。
7. Run evaluation and inspect matched or missing answer points.  
   运行评估并检查命中或缺失的答案要点。

## Demo Screenshots / 演示截图

Screenshots can be added under `docs/screenshots/` after running the local demo.

本地运行 demo 后，可以将截图放到 `docs/screenshots/` 目录。

| View / 页面 | Suggested File / 建议文件名 | Status / 状态 |
|---|---|---|
| FastAPI docs | `docs/screenshots/api-docs.png` | Placeholder |
| React upload and RAG Q&A | `docs/screenshots/react-rag-qa.png` | Placeholder |
| Agent steps and tool calls | `docs/screenshots/agent-workflow.png` | Placeholder |
| Structured report JSON | `docs/screenshots/structured-report.png` | Placeholder |
| Evaluation results | `docs/screenshots/evaluation-results.png` | Placeholder |

## Supporting Documents / 补充文档

- [Three minute demo script](docs/three_minute_demo_script.md)
- [Interview talking points](docs/interview_talking_points.md)
- [Recruiter summary](docs/recruiter_summary.md)

## Engineering Notes / 工程设计说明

FinAgent-RAG is organized as a small but complete financial research system instead of a single chat endpoint. The backend separates document ingestion, retrieval, stock-data tooling, agent orchestration, schemas, and evaluation, so each module can be tested and replaced independently.

FinAgent-RAG 按照一个小型但完整的金融研究系统来组织，而不是单一聊天接口。后端将文档处理、检索、股票数据工具、Agent 编排、schema 和评估模块拆开，方便独立测试和后续替换。

The RAG layer keeps answers grounded through chunk-level retrieval scores and citations. The report workflow records both agent steps and tool calls, making it easier to inspect how a final answer was assembled.

RAG 层通过文本块级别的检索分数和引用来源约束回答。报告工作流会记录 Agent 步骤和工具调用，便于追踪最终结论是如何生成的。

Structured reports are validated with Pydantic before being returned to the frontend. The evaluation module uses fixed questions, expected answer points, source coverage, and unknown-answer behavior to catch basic retrieval or hallucination issues.

结构化报告在返回前端前会经过 Pydantic 校验。评估模块使用固定问题、期望答案要点、来源覆盖和未知问题处理，检查基础检索质量与 hallucination 风险。

## Tests / 测试

```bash
pytest
```

Current tests cover:

- chunking
- retrieval relevance
- stock metrics
- API upload and RAG answer
- structured report and tool calls
- documents API
- evaluation API

## Extension Ideas / 后续扩展

- Replace hashing embeddings with OpenAI embeddings, bge, FAISS, Chroma, or pgvector.
- Add LangGraph for explicit graph state and retry control.
- Add real LLM calls with JSON mode or function calling.
- Add SEC filing ingestion and scheduled financial news collection.
- Add CI workflow for backend tests and frontend build.
- Add retrieval metrics such as recall@k, MRR, citation precision, and answer faithfulness.
