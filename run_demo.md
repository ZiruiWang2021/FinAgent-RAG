# Run Demo / 运行 Demo

This guide walks through the FinAgent-RAG demo from a clean terminal.  
本文档说明如何从零启动 FinAgent-RAG demo。

## 1. Install / 安装

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

## 2. Start FastAPI / 启动后端

```bash
uvicorn app.main:app --reload --port 8000
```

Check / 检查服务:

```bash
curl http://localhost:8000/health
```

## 3. Start Streamlit / 启动前端

Streamlit lightweight demo / Streamlit 轻量 demo:

```bash
streamlit run frontend/streamlit_app.py
```

React + TypeScript frontend / React + TypeScript 前端:

```bash
cd frontend-react
npm install
npm run dev
```

## 4. Demo Flow / 演示流程

1. Upload `data/sample_docs/demo_company.md`.  
   上传 `data/sample_docs/demo_company.md`。
2. Ask: `What drives ACME revenue growth?`  
   提问：`ACME 的收入增长由什么驱动？`
3. Ask: `What are the key risks?`  
   提问：`主要风险是什么？`
4. Enter ticker `AAPL` and click `Analyze Stock`.  
   输入股票代码 `AAPL`，点击 `Analyze Stock / 分析股票`。
5. Click `Generate Agent Report`.  
   点击生成 Agent 报告。
6. Review retrieved sources, stock metrics, agent steps, tool calls, structured JSON, and final report.  
   查看检索来源、股票指标、Agent 步骤、工具调用、结构化 JSON 和最终报告。
7. Run evaluation to inspect expected answer point coverage.  
   运行评估，查看期望答案要点覆盖情况。

## 5. API-Only Demo / 仅使用 API 的演示

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
