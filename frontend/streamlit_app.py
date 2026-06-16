"""Streamlit frontend for FinAgent-RAG."""

from __future__ import annotations

import requests
import streamlit as st


DEFAULT_API_BASE_URL = "http://localhost:8000"


st.set_page_config(page_title="FinAgent-RAG", layout="wide")
st.title("FinAgent-RAG")
st.caption("Multi-agent RAG analysis for financial documents and stock data / 面向金融文档和股票数据的多 Agent RAG 分析系统")


with st.sidebar:
    st.header("API / 接口")
    api_base_url = st.text_input("FastAPI URL / 后端地址", DEFAULT_API_BASE_URL)
    st.divider()
    st.header("Document Upload / 文档上传")
    uploaded_file = st.file_uploader("Upload txt, md, or pdf / 上传 txt、md 或 pdf", type=["txt", "md", "pdf"])
    if uploaded_file and st.button("Index document / 建立文档索引", use_container_width=True):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(f"{api_base_url}/upload", files=files, timeout=60)
        if response.ok:
            st.success(response.json()["message"])
        else:
            st.error(response.text)


left, right = st.columns([1, 1])

with left:
    st.subheader("Question / 问题")
    question = st.text_area(
        "Ask about company, industry, business model, financial performance, or risks / 可询问公司、行业、商业模式、财务表现或风险",
        value="What are the main business drivers and risk factors?",
        height=120,
    )
    ticker = st.text_input("Ticker / 股票代码", value="AAPL")
    top_k = st.slider("Retrieved chunks / 检索片段数", min_value=1, max_value=10, value=4)

    ask_clicked = st.button("Ask RAG / RAG 问答", use_container_width=True)
    stock_clicked = st.button("Analyze Stock / 分析股票", use_container_width=True)
    report_clicked = st.button("Run Agent Workflow / 运行 Agent 工作流", use_container_width=True)

with right:
    st.subheader("Results / 结果")

    if ask_clicked:
        payload = {"question": question, "top_k": top_k}
        response = requests.post(f"{api_base_url}/ask", json=payload, timeout=60)
        if response.ok:
            result = response.json()
            st.markdown(result["answer"])
            with st.expander("Sources / 引用来源", expanded=True):
                for source in result["sources"]:
                    st.markdown(f"**{source['source']}** · score `{source['score']}`")
                    st.write(source["content"])
        else:
            st.error(response.text)

    if stock_clicked:
        payload = {"ticker": ticker, "period": "6mo"}
        response = requests.post(f"{api_base_url}/analyze-stock", json=payload, timeout=60)
        if response.ok:
            metrics = response.json()["metrics"]
            metric_cols = st.columns(3)
            metric_cols[0].metric("1M Return / 1个月收益", f"{metrics['one_month_return_pct']}%")
            metric_cols[1].metric("Volatility / 波动率", f"{metrics['annualized_volatility_pct']}%")
            metric_cols[2].metric("Max Drawdown / 最大回撤", f"{metrics['max_drawdown_pct']}%")
            st.json(metrics)
        else:
            st.error(response.text)

    if report_clicked:
        payload = {"question": question, "ticker": ticker or None, "top_k": top_k}
        response = requests.post(f"{api_base_url}/generate-report", json=payload, timeout=120)
        if response.ok:
            result = response.json()
            st.markdown(result["report"])
            with st.expander("Agent Steps / Agent 步骤", expanded=True):
                for step in result["steps"]:
                    st.markdown(f"**{step['agent']}** · {step['action']}")
                    st.text(step["output"])
        else:
            st.error(response.text)
