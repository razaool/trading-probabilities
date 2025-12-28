import axios from 'axios';
import type { QueryRequest, QueryResponse, TickerListResponse, TickerSuggestion, TickerSuggestionsResponse } from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  async queryHistoricalPatterns(request: QueryRequest): Promise<QueryResponse> {
    const response = await api.post('/api/query', request);
    return response.data;
  },

  async getAvailableTickers(): Promise<TickerListResponse> {
    const response = await api.get('/api/tickers');
    return response.data;
  },

  async getTickerSuggestions(query: string): Promise<TickerSuggestion[]> {
    const response = await api.get('/api/tickers/suggest', { params: { q: query } });
    return response.data.suggestions;
  },

  async getEtfConstituents(etfTicker: string): Promise<{ etf: string; constituents: string[]; count: number }> {
    const response = await api.get(`/api/tickers/etf/${etfTicker}`);
    return response.data;
  },

  async getHistoricalPrices(ticker: string): Promise<{ ticker: string; prices: Array<{ date: string; open: number; high: number; low: number; close: number; volume: number }> }> {
    const response = await api.get(`/api/prices/${ticker}`);
    return response.data;
  },

  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get('/health');
    return response.data;
  },
};
