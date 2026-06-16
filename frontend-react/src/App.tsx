import { useState } from 'react';
import { askRag, generateReport, runEvaluation, uploadDocument } from './api';
import type { AskResponse, EvaluationResponse, ReportResponse } from './types';

const DEFAULT_API = 'http://localhost:8000';
const text = {
  subtitle:
    'AI Native financial news and research workflow / AI Native 金融资讯与研究分析工作流',
  apiBaseUrl: 'API Base URL / 后端接口地址',
  upload: 'Upload document / 上传文档',
  question: 'Analysis question / 分析问题',
  ticker: 'Ticker / 股票代码',
  topK: 'Top K / 检索条数',
  ask: 'Run RAG Q&A / 运行 RAG 问答',
  report: 'Generate Agent Report / 生成 Agent 报告',
  evaluate: 'Run Evaluation / 运行评估',
  ragAnswer: 'RAG Answer / RAG 回答',
  citations: 'Citations / 引用来源',
  agentSteps: 'Agent Steps / Agent 步骤',
  toolCalls: 'Tool Calls / 工具调用',
  structuredReport: 'Structured Report / 结构化报告',
  evaluation: 'Evaluation / 模型评估'
};

export default function App() {
  const [apiBaseUrl, setApiBaseUrl] = useState(DEFAULT_API);
  const [question, setQuestion] = useState('What are ACME growth drivers and risks?');
  const [ticker, setTicker] = useState('AAPL');
  const [topK, setTopK] = useState(4);
  const [status, setStatus] = useState('');
  const [askResult, setAskResult] = useState<AskResponse | null>(null);
  const [reportResult, setReportResult] = useState<ReportResponse | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null);

  async function handleUpload(file: File | null) {
    if (!file) return;
    setStatus('Uploading and indexing document... / 正在上传并索引文档...');
    const result = await uploadDocument(apiBaseUrl, file);
    setStatus(`${result.filename}: indexed ${result.chunks_indexed} chunks / 已索引 ${result.chunks_indexed} 个文本块`);
  }

  async function handleAsk() {
    setStatus('Running RAG retrieval... / 正在执行 RAG 检索...');
    const result = await askRag(apiBaseUrl, question, topK);
    setAskResult(result);
    setStatus(`Retrieved ${result.sources.length} sources / 检索到 ${result.sources.length} 个来源`);
  }

  async function handleReport() {
    setStatus('Running agent workflow... / 正在执行 Agent 工作流...');
    const result = await generateReport(apiBaseUrl, question, ticker, topK);
    setReportResult(result);
    setStatus(`Generated report with ${result.steps.length} agent steps / 已生成 ${result.steps.length} 个 Agent 步骤`);
  }

  async function handleEvaluation() {
    setStatus('Running evaluation cases... / 正在运行评估用例...');
    const result = await runEvaluation(apiBaseUrl);
    setEvaluation(result);
    setStatus(`Evaluation passed ${result.passed_cases}/${result.total_cases} / 评估通过 ${result.passed_cases}/${result.total_cases}`);
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <h1>FinAgent-RAG</h1>
          <p>{text.subtitle}</p>
        </div>
        <label className="api-input">
          {text.apiBaseUrl}
          <input value={apiBaseUrl} onChange={(event) => setApiBaseUrl(event.target.value)} />
        </label>
      </header>

      <section className="workspace">
        <aside className="control-panel">
          <label>
            {text.upload}
            <input type="file" accept=".txt,.md,.pdf" onChange={(event) => handleUpload(event.target.files?.[0] ?? null)} />
          </label>

          <label>
            {text.question}
            <textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows={5} />
          </label>

          <div className="grid-two">
            <label>
              {text.ticker}
              <input value={ticker} onChange={(event) => setTicker(event.target.value.toUpperCase())} />
            </label>
            <label>
              {text.topK}
              <input type="number" min={1} max={10} value={topK} onChange={(event) => setTopK(Number(event.target.value))} />
            </label>
          </div>

          <button onClick={handleAsk}>{text.ask}</button>
          <button onClick={handleReport}>{text.report}</button>
          <button onClick={handleEvaluation}>{text.evaluate}</button>
          <p className="status">{status}</p>
        </aside>

        <section className="results">
          {askResult && (
            <article className="panel">
              <h2>{text.ragAnswer}</h2>
              <pre>{askResult.answer}</pre>
              <h3>{text.citations}</h3>
              <div className="list">
                {askResult.sources.map((source) => (
                  <div className="source" key={source.chunk_id}>
                    <strong>{source.source}</strong>
                    <span>score {source.score}</span>
                    <p>{source.content}</p>
                  </div>
                ))}
              </div>
            </article>
          )}

          {reportResult && (
            <>
              <article className="panel">
                <h2>{text.agentSteps}</h2>
                <div className="list">
                  {reportResult.steps.map((step) => (
                    <div className="source" key={`${step.agent}-${step.action}`}>
                      <strong>{step.agent}</strong>
                      <span>{step.action}</span>
                      <p>{step.output}</p>
                    </div>
                  ))}
                </div>
              </article>

              <article className="panel">
                <h2>{text.toolCalls}</h2>
                <div className="list">
                  {reportResult.tool_calls.map((call) => (
                    <div className="source" key={`${call.tool_name}-${call.output_summary}`}>
                      <strong>{call.tool_name}</strong>
                      <span>{call.status}</span>
                      <code>{JSON.stringify(call.input)}</code>
                      <p>{call.output_summary}</p>
                    </div>
                  ))}
                </div>
              </article>

              <article className="panel">
                <h2>{text.structuredReport}</h2>
                <pre>{JSON.stringify(reportResult.structured_report, null, 2)}</pre>
              </article>
            </>
          )}

          {evaluation && (
            <article className="panel">
              <h2>{text.evaluation}</h2>
              <p>
                Passed {evaluation.passed_cases}/{evaluation.total_cases}; average groundedness{' '}
                {evaluation.average_groundedness_score}
              </p>
              <div className="list">
                {evaluation.results.map((result) => (
                  <div className="source" key={result.case_id}>
                    <strong>{result.case_id}</strong>
                    <span>{result.passed ? 'passed' : 'needs review'}</span>
                    <p>{result.question}</p>
                    <small>Matched: {result.matched_points.join(', ') || 'none'}</small>
                  </div>
                ))}
              </div>
            </article>
          )}
        </section>
      </section>
    </main>
  );
}
