import { useState } from 'react';
import { askRag, generateReport, runEvaluation, uploadDocument } from './api';
import type { AskResponse, EvaluationResponse, ReportResponse } from './types';

const DEFAULT_API = 'http://localhost:8000';

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
    setStatus('Uploading and indexing document...');
    const result = await uploadDocument(apiBaseUrl, file);
    setStatus(`${result.filename}: indexed ${result.chunks_indexed} chunks`);
  }

  async function handleAsk() {
    setStatus('Running RAG retrieval...');
    const result = await askRag(apiBaseUrl, question, topK);
    setAskResult(result);
    setStatus(`Retrieved ${result.sources.length} sources`);
  }

  async function handleReport() {
    setStatus('Running agent workflow...');
    const result = await generateReport(apiBaseUrl, question, ticker, topK);
    setReportResult(result);
    setStatus(`Generated report with ${result.steps.length} agent steps`);
  }

  async function handleEvaluation() {
    setStatus('Running evaluation cases...');
    const result = await runEvaluation(apiBaseUrl);
    setEvaluation(result);
    setStatus(`Evaluation passed ${result.passed_cases}/${result.total_cases}`);
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <h1>FinAgent-RAG</h1>
          <p>AI Native financial news and research workflow with RAG, tools, agents, and structured output.</p>
        </div>
        <label className="api-input">
          API Base URL
          <input value={apiBaseUrl} onChange={(event) => setApiBaseUrl(event.target.value)} />
        </label>
      </header>

      <section className="workspace">
        <aside className="control-panel">
          <label>
            Upload document
            <input type="file" accept=".txt,.md,.pdf" onChange={(event) => handleUpload(event.target.files?.[0] ?? null)} />
          </label>

          <label>
            Analysis question
            <textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows={5} />
          </label>

          <div className="grid-two">
            <label>
              Ticker
              <input value={ticker} onChange={(event) => setTicker(event.target.value.toUpperCase())} />
            </label>
            <label>
              Top K
              <input type="number" min={1} max={10} value={topK} onChange={(event) => setTopK(Number(event.target.value))} />
            </label>
          </div>

          <button onClick={handleAsk}>Run RAG Q&A</button>
          <button onClick={handleReport}>Generate Agent Report</button>
          <button onClick={handleEvaluation}>Run Evaluation</button>
          <p className="status">{status}</p>
        </aside>

        <section className="results">
          {askResult && (
            <article className="panel">
              <h2>RAG Answer</h2>
              <pre>{askResult.answer}</pre>
              <h3>Citations</h3>
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
                <h2>Agent Steps</h2>
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
                <h2>Tool Calls</h2>
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
                <h2>Structured Report</h2>
                <pre>{JSON.stringify(reportResult.structured_report, null, 2)}</pre>
              </article>
            </>
          )}

          {evaluation && (
            <article className="panel">
              <h2>Evaluation</h2>
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
