export type RetrievedChunk = {
  chunk_id: string;
  source: string;
  content: string;
  score: number;
};

export type Citation = {
  source: string;
  chunk_id: string;
  score: number;
  quote: string;
};

export type ToolCallRecord = {
  tool_name: string;
  input: Record<string, unknown>;
  output_summary: string;
  status: string;
};

export type StockMetrics = {
  ticker: string;
  start_date: string;
  end_date: string;
  latest_close: number;
  one_month_return_pct: number;
  annualized_volatility_pct: number;
  ma20: number;
  ma60: number;
  max_drawdown_pct: number;
  trend: string;
};

export type WorkflowStep = {
  agent: string;
  action: string;
  output: string;
};

export type StructuredReport = {
  title: string;
  executive_summary: string;
  key_findings: string[];
  risks: Array<{ name: string; severity: string; evidence: string }>;
  citations: Citation[];
  stock_metrics?: StockMetrics | null;
  hallucination_controls: string[];
};

export type AskResponse = {
  question: string;
  answer: string;
  sources: RetrievedChunk[];
};

export type ReportResponse = {
  question: string;
  ticker?: string | null;
  steps: WorkflowStep[];
  report: string;
  sources: RetrievedChunk[];
  stock_analysis?: StockMetrics | null;
  tool_calls: ToolCallRecord[];
  structured_report?: StructuredReport | null;
};

export type EvaluationResponse = {
  total_cases: number;
  passed_cases: number;
  average_groundedness_score: number;
  results: Array<{
    case_id: string;
    question: string;
    expected_answer_points: string[];
    matched_points: string[];
    missing_points: string[];
    source_count: number;
    groundedness_score: number;
    passed: boolean;
    answer_preview: string;
  }>;
};
