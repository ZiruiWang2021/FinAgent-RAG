# Three Minute Demo Script / 三分钟演示脚本

This script is written for a short walkthrough of FinAgent-RAG. It focuses on what the system does, how the workflow is observable, and where the current prototype is intentionally simple.

本文档用于三分钟快速演示 FinAgent-RAG。重点说明系统能力、工作流可观测性，以及当前原型的边界。

## 0:00 - 0:20 Project Context / 项目背景

FinAgent-RAG is a financial document research workflow. It supports document upload, RAG Q&A with citations, stock-data tool calls, a simple multi-agent report workflow, structured output, and basic evaluation.

FinAgent-RAG 是一个金融文档研究工作流，支持文档上传、带引用来源的 RAG 问答、股票数据工具调用、简单多 Agent 报告生成、结构化输出和基础评估。

## 0:20 - 0:50 Upload And Index / 上传与索引

1. Start the FastAPI backend.
2. Open the React frontend.
3. Upload `data/sample_docs/demo_company.md`.
4. Mention that the backend extracts text, chunks it, embeds chunks, and stores them in the local vector store.

演示时说明：上传文档后，后端会完成文本读取、chunking、embedding 和本地向量索引。

## 0:50 - 1:30 RAG Q&A / RAG 问答

Ask:

```text
What drives ACME revenue growth?
```

Show:

- answer text
- retrieved chunks
- source names
- retrieval scores

Then ask:

```text
What is ACME's dividend policy?
```

Use this question to show that the system should avoid inventing unsupported details when the document library does not contain enough evidence.

## 1:30 - 2:20 Agent Report / Agent 报告

Use ticker:

```text
AAPL
```

Ask:

```text
Summarize ACME growth drivers, risks, and market context.
```

Click `Generate Agent Report / 生成 Agent 报告`.

Show:

- Planner, Retriever, Data, Risk, and Report agent steps
- document retrieval and stock data tool-call records
- structured report JSON validated by Pydantic
- citations and stock metrics inside the final report payload

## 2:20 - 2:45 Evaluation / 评估

Click `Run Evaluation / 运行评估`.

Explain that the evaluation module uses fixed questions, expected answer points, source coverage, and groundedness scoring. It is not a full benchmark, but it is enough to catch basic retrieval quality and hallucination-control issues in this prototype.

## 2:45 - 3:00 Code Structure / 代码结构

Briefly show:

```text
app/rag/
app/agents/
app/tools/
app/schemas/models.py
app/evaluation/
frontend-react/src/
tests/
```

Close with the current limitations: local hashing embeddings, in-memory vector store, and lightweight rule-based report generation. These choices keep the project runnable without paid APIs and make it easy to replace components later.
