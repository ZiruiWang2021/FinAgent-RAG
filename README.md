# FinAgent-RAG

FinAgent-RAG is a production-oriented multi-agent RAG system for financial research reports, company announcements, and stock market data.

FinAgent-RAG 是一个面向金融研报、公司公告和股票数据的多 Agent 智能分析系统，重点展示 RAG、工具调用、任务编排、数据分析、API 服务和前端交互的完整工程实现。

> This project is for engineering demonstration and research workflow prototyping only. It is not investment advice.  
> 本项目仅用于工程实践展示和研究流程原型验证，不构成任何投资建议。

## Project Highlights / 项目亮点

- **Multi-agent workflow / 多 Agent 工作流**: Planner, Retriever, Data, Risk, and Report agents cooperate to complete an end-to-end financial analysis task.
- **Source-grounded RAG / 基于来源的 RAG**: uploaded documents are extracted, chunked, embedded, retrieved, and cited in answers.
- **Tool calling / 工具调用**: the Data Agent calls a stock data tool backed by `yfinance`.
- **Financial metrics / 金融指标计算**: 1-month return, annualized volatility, MA20, MA60, maximum drawdown, and trend signal.
- **FastAPI backend / FastAPI 后端**: modular API routers with Pydantic request and response schemas.
- **Streamlit frontend / Streamlit 前端**: document upload, question answering, stock analysis, workflow trace, and final report in one demo UI.
- **Evaluation examples / 评估样例**: controlled sample document and tests help check retrieval quality and reduce hallucination risk.
- **Extensible structure / 可扩展结构**: local hashing embeddings can be replaced with OpenAI embeddings, FAISS, Chroma, pgvector, LangChain, or LlamaIndex.

## Use Cases / 适用场景

- Summarize company research reports and announcements.  
  汇总公司研报和公告中的关键信息。
- Answer questions about business model, industry drivers, financial performance, and risks.  
  回答商业模式、行业驱动、财务表现和风险因素相关问题。
- Combine document evidence with market data analysis.  
  将文档证据与股票市场数据分析结合起来。
- Prototype enterprise AI workflows that need retrieval, tool calling, and report generation.  
  原型验证需要检索、工具调用和报告生成的企业级 AI 工作流。

## Tech Stack / 技术栈

- Python
- FastAPI
- Streamlit
- Pydantic
- pandas / numpy
- yfinance
- pypdf
- pytest

The current retriever uses deterministic hashing embeddings so the project runs without API keys or model downloads. In production, the `app/rag/` boundary can be replaced with OpenAI embeddings, SentenceTransformers, FAISS, Chroma, pgvector, LangChain, or LlamaIndex.

当前检索器使用确定性的 hashing embedding，因此无需 API key 或模型下载即可运行。生产环境中可以在 `app/rag/` 边界替换为 OpenAI Embeddings、SentenceTransformers、FAISS、Chroma、pgvector、LangChain 或 LlamaIndex。

## Repo Structure / 项目结构

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

## Architecture / 架构说明

```text
User / 用户
  |
  | Streamlit frontend / 前端交互
  v
FastAPI backend / 后端服务
  |
  +-- POST /upload
  |     document_loader -> chunker -> embeddings -> vector_store
  |     文档加载 -> 文本切分 -> 向量化 -> 向量检索库
  |
  +-- POST /ask
  |     retriever -> source-grounded RAG answer
  |     检索器 -> 带引用来源的 RAG 回答
  |
  +-- POST /analyze-stock
  |     stock_data_tool -> financial_metrics
  |     股票数据工具 -> 金融指标计算
  |
  +-- POST /generate-report
        Planner Agent  / 任务规划
          -> Retriever Agent / 文档检索
          -> Data Agent      / 数据分析
          -> Risk Agent      / 风险总结
          -> Report Agent    / 报告生成
```

## Core Features / 核心功能

1. Upload `txt`, `md`, and `pdf` documents.  
   支持上传 `txt`、`md` 和 `pdf` 文档。
2. Extract text, chunk documents, embed chunks, and retrieve relevant passages.  
   支持文本抽取、chunking、embedding 和相关片段检索。
3. Answer company, industry, risk, business model, and financial performance questions with citations.  
   支持围绕公司、行业、风险、商业模式和财务表现进行带引用回答。
4. Analyze stock data with return, volatility, moving averages, drawdown, and trend.  
   支持股票收益率、波动率、均线、最大回撤和趋势判断。
5. Run a multi-agent workflow with observable intermediate steps.  
   支持可观察的多 Agent 工作流步骤。
6. Provide both API and UI entry points.  
   同时提供 API 和前端界面入口。

## Installation / 安装

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

## Run the Backend / 启动后端

```bash
uvicorn app.main:app --reload --port 8000
```

Health check / 健康检查:

```bash
curl http://localhost:8000/health
```

## Run the Frontend / 启动前端

In a second terminal / 在第二个终端中运行:

```bash
streamlit run frontend/streamlit_app.py
```

Open the Streamlit URL shown in the terminal, usually `http://localhost:8501`.  
打开终端中显示的 Streamlit 地址，通常是 `http://localhost:8501`。

## API Examples / API 示例

Upload a document / 上传文档:

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@data/sample_docs/demo_company.md"
```

Ask a RAG question / 提问:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What are ACME growth drivers and risks?","top_k":4}'
```

Analyze a stock / 分析股票:

```bash
curl -X POST http://localhost:8000/analyze-stock \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","period":"6mo"}'
```

Generate a report / 生成报告:

```bash
curl -X POST http://localhost:8000/generate-report \
  -H "Content-Type: application/json" \
  -d '{"question":"Analyze ACME business drivers, financial performance, and key risks.","ticker":"AAPL","top_k":4}'
```

## Demo Questions / Demo 问题

- What are the main revenue growth drivers?  
  主要收入增长驱动因素是什么？
- What risks does the company disclose?  
  公司披露了哪些风险？
- How does the company describe its business model?  
  公司如何描述其商业模式？
- What financial performance trend is mentioned in the report?  
  报告中提到了哪些财务表现趋势？
- What industry headwinds or regulatory risks should investors monitor?  
  需要关注哪些行业压力或监管风险？
- Generate a structured report and include market data for `AAPL`.  
  生成结构化报告，并加入 `AAPL` 的市场数据分析。

## Evaluation Examples / 评估样例

Use `data/sample_docs/demo_company.md` as a small controlled document set.  
可以使用 `data/sample_docs/demo_company.md` 作为小型可控文档集。

- Ask: `What drives ACME revenue growth?`  
  提问：`ACME 的收入增长由什么驱动？`
  - Expected evidence should mention cloud software subscriptions and enterprise customer expansion.  
    期望证据应提到云软件订阅和企业客户扩张。
- Ask: `What are ACME's main risks?`  
  提问：`ACME 的主要风险是什么？`
  - Expected evidence should mention competition, customer concentration, sales cycle uncertainty, or margin pressure.  
    期望证据应提到竞争、客户集中度、销售周期不确定性或利润率压力。
- Ask: `What is ACME's dividend policy?`  
  提问：`ACME 的分红政策是什么？`
  - Expected behavior should be cautious because the sample document does not contain this information.  
    由于样例文档不包含该信息，系统应给出谨慎回答。

## Tests / 测试

```bash
pytest
```

The test suite covers / 测试覆盖:

- document chunking / 文档切分
- retrieval relevance / 检索相关性
- stock indicator calculations / 股票指标计算
- FastAPI upload, RAG answer, stock analysis, and report generation / FastAPI 上传、RAG 回答、股票分析和报告生成

## Extension Ideas / 后续扩展

- Replace local hashing embeddings with OpenAI embeddings plus FAISS or Chroma.  
  将本地 hashing embedding 替换为 OpenAI Embeddings + FAISS 或 Chroma。
- Add persistent document collections and metadata filters by company, date, sector, and document type.  
  增加持久化文档库，并按公司、日期、行业、文档类型过滤。
- Use LangGraph or CrewAI for richer multi-agent planning, retries, and state transitions.  
  使用 LangGraph 或 CrewAI 扩展多 Agent 状态流转、重试和计划能力。
- Add SEC filing ingestion, earnings transcript parsing, and scheduled market data refresh.  
  增加 SEC 文件解析、业绩会文字稿解析和定时市场数据刷新。
- Add structured evaluation datasets for retrieval quality, citation coverage, and hallucination detection.  
  增加结构化评估集，用于检索质量、引用覆盖率和幻觉检测。
- Add authentication, rate limiting, background jobs, observability, and deployment manifests.  
  增加认证、限流、后台任务、可观测性和部署配置。
