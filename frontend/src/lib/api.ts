/**
 * API client for backend communication
 */

import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API response types
export interface Recommendation {
  ticker: string
  name: string
  action: string
  price: number
  target: number
  stop_loss: number
  total_score: number
  technical_score: number
  fundamental_score: number
  catalyst_score: number
  reasoning: string
  catalyst: string
  risk_reward: number
  position_size: string
}

export interface DailyDigest {
  date: string
  generated_at: string
  market_summary: {
    overnight_moves: {
      sp500_change: number
      nasdaq_change: number
      dow_change: number
    }
    key_driver: string
  }
  top_recommendation: Recommendation
  watch_list: Array<{
    ticker: string
    reason: string
    score: number
  }>
  key_events: Array<{
    time: string
    event: string
    expected_impact: string
  }>
  macro_context: {
    fed_policy: string
    inflation: string
    sentiment: string
  }
}

export interface StockDetails {
  ticker: string
  name: string
  price: {
    current: number
    change: number
    change_percent: number
  }
  fundamentals: {
    pe_ratio: number
    pb_ratio: number
    roe: number
    revenue_growth: number
  }
  technicals: {
    rsi: number
    macd: number
    trend: string
  }
}

// API endpoints
export const digestApi = {
  getToday: () => api.get<DailyDigest>('/api/digest/today'),
  getHistory: (limit = 30) => api.get<any>('/api/digest/history', { params: { limit } }),
  getPerformance: () => api.get<any>('/api/digest/performance'),
}

export const stocksApi = {
  getDetails: (ticker: string) => api.get<StockDetails>(`/api/stocks/${ticker}`),
  getHistory: (ticker: string, params?: any) =>
    api.get<any>(`/api/stocks/${ticker}/history`, { params }),
  getNews: (ticker: string, limit = 10) =>
    api.get<any>(`/api/stocks/${ticker}/news`, { params: { limit } }),
  getFilings: (ticker: string, filing_type?: string) =>
    api.get<any>(`/api/stocks/${ticker}/filings`, { params: { filing_type } }),
}

export const eventsApi = {
  getEarningsCalendar: (start_date?: string, end_date?: string) =>
    api.get<any>('/api/events/earnings', { params: { start_date, end_date } }),
  getRecentFilings: (filing_type?: string, days = 7) =>
    api.get<any>('/api/events/filings/recent', { params: { filing_type, days } }),
  getMacroEvents: (start_date?: string, end_date?: string) =>
    api.get<any>('/api/events/macro', { params: { start_date, end_date } }),
  getInsiderTrading: (ticker?: string, days = 30) =>
    api.get<any>('/api/events/insider-trading', { params: { ticker, days } }),
}
