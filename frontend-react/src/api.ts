import type { AskResponse, EvaluationResponse, ReportResponse } from './types';

export async function uploadDocument(apiBaseUrl: string, file: File) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await fetch(`${apiBaseUrl}/upload`, {
    method: 'POST',
    body: formData
  });
  return parseJson(response);
}

export async function askRag(apiBaseUrl: string, question: string, topK: number): Promise<AskResponse> {
  const response = await fetch(`${apiBaseUrl}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k: topK })
  });
  return parseJson(response);
}

export async function generateReport(
  apiBaseUrl: string,
  question: string,
  ticker: string,
  topK: number
): Promise<ReportResponse> {
  const response = await fetch(`${apiBaseUrl}/generate-report`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, ticker: ticker || null, top_k: topK })
  });
  return parseJson(response);
}

export async function runEvaluation(apiBaseUrl: string): Promise<EvaluationResponse> {
  const response = await fetch(`${apiBaseUrl}/evaluate`, { method: 'POST' });
  return parseJson(response);
}

async function parseJson(response: Response) {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }
  return response.json();
}
