export interface QueryRequest {
  ticker: string;
  condition_type: 'percentage_change' | 'absolute_threshold';
  threshold: number;
  operator: 'gt' | 'lt' | 'gte' | 'lte' | 'eq';
  time_horizons?: ('1d' | '1w' | '1m' | '1y')[];
}

export interface PatternInstance {
  date: string;
  forward_returns: Record<string, number | null>;
}

export interface SummaryStatistics {
  mean: number;
  median: number;
  std: number;
  min: number;
  max: number;
  win_rate: number;
  count: number;
}

export interface QueryResponse {
  ticker: string;
  condition: string;
  reference_ticker?: string;
  instances: PatternInstance[];
  summary_statistics: Record<string, SummaryStatistics>;
  total_occurrences: number;
}

export interface TickerListResponse {
  market_indices: string[];
  sector_etfs: string[];
  volatility_indicators: string[];
  sentiment_indicators: string[];
  commodities: string[];
  top_stocks: string[];
}
