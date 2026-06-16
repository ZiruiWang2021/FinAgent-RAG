# Interview Talking Points / 项目讲解要点

These notes are for explaining FinAgent-RAG clearly and honestly. They avoid overstating the project as a production-grade platform.

本文档用于清楚、真实地讲解 FinAgent-RAG，避免把项目夸大成生产级平台。

## One Sentence / 一句话介绍

FinAgent-RAG is a small full-stack financial research assistant that combines document RAG, stock-data tool calls, a visible agent workflow, structured report output, and lightweight evaluation.

FinAgent-RAG 是一个小型全栈金融研究助手，组合了文档 RAG、股票数据工具调用、可观测 Agent 工作流、结构化报告输出和轻量评估。

## What To Emphasize / 重点说明

- The project is end-to-end: FastAPI backend, React frontend, RAG pipeline, tools, agents, schemas, tests, and documentation.
- The answer path is inspectable: users can see retrieved chunks, citations, agent steps, and tool calls.
- Structured output is validated with Pydantic instead of returning arbitrary text only.
- The evaluation module is simple but useful: fixed questions, expected answer points, source coverage, and unknown-answer behavior.
- The frontend is intentionally simple so the demo focuses on workflow transparency, not visual polish.

## Technical Decisions / 技术决策

- Local hashing embeddings keep the project easy to run without external API keys.
- The vector store is in memory for clarity and testability.
- Agent classes are lightweight Python modules instead of a heavy orchestration framework.
- Prompt files are separated from agent code to make prompt iteration visible.
- Stock metrics are computed as a deterministic tool call, separate from RAG text retrieval.

## Tradeoffs / 取舍

- The retrieval backend is not designed for large-scale document collections.
- The current report generator is deterministic and template-based, not a production LLM reasoning system.
- The evaluation set is intentionally small and should be expanded before serious quality claims.
- yfinance data depends on network availability and upstream data behavior.
- The project prioritizes readable architecture over advanced optimization.

## Good Questions To Be Ready For / 可能被问到的问题

**Why not use LangGraph now?**  
The current workflow is small enough to keep explicit in plain Python. LangGraph would be a natural next step if retries, branching, memory, or long-running state become necessary.

**How would you reduce hallucination further?**  
Use stronger embeddings, citation precision checks, answer abstention thresholds, LLM-as-judge or human-labeled evals, and stricter structured-output validation.

**How would you scale this?**  
Replace the in-memory vector store with Chroma, FAISS, pgvector, or a managed vector DB; persist document metadata; add background ingestion; and add API auth plus observability.

**What would you improve first?**  
Add a real embedding model, expand evaluation cases, add CI for backend tests and frontend build, and capture demo screenshots for README.

## Honest Positioning / 真实定位

This is a portfolio-ready prototype that demonstrates core AI application patterns. It is not a trading system, investment platform, or production financial research product.

这是一个适合作品集展示的原型项目，用于体现 AI 应用开发中的核心模式。它不是交易系统、投资平台或生产级金融研究产品。
