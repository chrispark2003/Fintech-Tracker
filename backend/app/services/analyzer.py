"""
Stock analysis service - The intelligence layer (your competitive moat)

This is where you build the attribution engine that answers "WHY did this stock move?"
"""

from typing import Dict, List
import pandas as pd
import pandas_ta as ta


class StockAnalyzer:
    """
    Analyzes stocks and generates scores

    This is YOUR secret sauce - the logic that combines signals into recommendations
    """

    def calculate_technical_score(self, price_data: pd.DataFrame) -> float:
        """
        Calculate technical score (0-10)

        Factors:
        - Trend strength (moving averages)
        - Momentum (RSI, MACD)
        - Volume patterns
        - Support/resistance levels
        """
        if price_data.empty:
            return 0.0

        score = 0.0

        try:
            # Add technical indicators
            price_data.ta.rsi(length=14, append=True)
            price_data.ta.macd(append=True)
            price_data.ta.sma(length=50, append=True)
            price_data.ta.sma(length=200, append=True)

            # RSI score (optimal range: 40-70)
            latest_rsi = price_data['RSI_14'].iloc[-1]
            if 40 <= latest_rsi <= 70:
                score += 3.0
            elif latest_rsi < 30:  # Oversold
                score += 1.5
            elif latest_rsi > 70:  # Overbought
                score += 1.0

            # Trend score (price above moving averages)
            latest_price = price_data['close'].iloc[-1]
            sma_50 = price_data['SMA_50'].iloc[-1]
            sma_200 = price_data['SMA_200'].iloc[-1]

            if latest_price > sma_50 > sma_200:  # Strong uptrend
                score += 4.0
            elif latest_price > sma_50:
                score += 2.0

            # Volume score (above average = conviction)
            avg_volume = price_data['volume'].mean()
            recent_volume = price_data['volume'].iloc[-5:].mean()
            if recent_volume > avg_volume * 1.2:
                score += 3.0

        except Exception as e:
            print(f"Error calculating technical score: {e}")

        return min(score, 10.0)  # Cap at 10

    def calculate_fundamental_score(self, fundamentals: Dict) -> float:
        """
        Calculate fundamental score (0-10)

        Factors:
        - Valuation (P/E, P/B relative to sector)
        - Profitability (ROE, margins)
        - Growth (revenue, earnings growth)
        - Financial health (debt levels, cash flow)
        """
        if not fundamentals:
            return 0.0

        score = 0.0

        try:
            # Valuation score (lower P/E is better, but not too low)
            pe_ratio = fundamentals.get('peRatio', 0)
            if 10 <= pe_ratio <= 25:
                score += 3.0
            elif 5 <= pe_ratio < 10 or 25 < pe_ratio <= 35:
                score += 1.5

            # Profitability score
            roe = fundamentals.get('returnOnEquity', 0)
            if roe > 0.15:  # >15% ROE is good
                score += 3.0
            elif roe > 0.10:
                score += 2.0

            # Growth score
            revenue_growth = fundamentals.get('revenueGrowth', 0)
            if revenue_growth > 0.15:  # >15% growth
                score += 4.0
            elif revenue_growth > 0.05:
                score += 2.0

        except Exception as e:
            print(f"Error calculating fundamental score: {e}")

        return min(score, 10.0)

    def calculate_catalyst_score(
        self,
        news: List[Dict],
        filings: List[Dict],
        earnings: Dict
    ) -> float:
        """
        Calculate catalyst score (0-10)

        Factors:
        - Recent 8-K filings (material events)
        - Earnings beats/misses
        - News sentiment
        - Analyst upgrades/downgrades
        """
        score = 0.0

        # News sentiment
        if news:
            avg_sentiment = sum(n.get('sentiment', 0) for n in news[:10]) / min(len(news), 10)
            if avg_sentiment > 0.3:
                score += 3.0
            elif avg_sentiment > 0:
                score += 1.5

        # Recent material 8-K filings
        recent_8k = [f for f in filings if f.get('type') == '8-K']
        if recent_8k:
            score += 3.0

        # Earnings catalyst
        if earnings:
            eps_surprise = earnings.get('eps_surprise_percent', 0)
            if eps_surprise > 5:  # Beat by >5%
                score += 4.0
            elif eps_surprise > 0:
                score += 2.0

        return min(score, 10.0)

    def generate_recommendation(
        self,
        ticker: str,
        technical_score: float,
        fundamental_score: float,
        catalyst_score: float,
        weights: Dict = None
    ) -> Dict:
        """
        Generate final recommendation based on scores

        Default weights: 40% technical, 40% fundamental, 20% catalyst
        """
        if weights is None:
            weights = {"technical": 0.4, "fundamental": 0.4, "catalyst": 0.2}

        total_score = (
            technical_score * weights["technical"] +
            fundamental_score * weights["fundamental"] +
            catalyst_score * weights["catalyst"]
        )

        # Determine action
        if total_score >= 8.0:
            action = "STRONG BUY"
        elif total_score >= 6.5:
            action = "BUY"
        elif total_score >= 5.0:
            action = "HOLD"
        elif total_score >= 3.0:
            action = "WATCH"
        else:
            action = "AVOID"

        return {
            "ticker": ticker,
            "total_score": round(total_score, 2),
            "technical_score": round(technical_score, 2),
            "fundamental_score": round(fundamental_score, 2),
            "catalyst_score": round(catalyst_score, 2),
            "action": action,
            "weights": weights
        }

    def detect_why(
        self,
        ticker: str,
        price_change_percent: float,
        recent_events: Dict
    ) -> str:
        """
        THE ATTRIBUTION ENGINE - Answers "WHY did this stock move?"

        This is your competitive moat - linking price movements to catalysts

        Args:
            ticker: Stock symbol
            price_change_percent: % change in price
            recent_events: Dict with news, filings, earnings, etc.

        Returns:
            Human-readable explanation
        """
        reasons = []

        # Check for earnings
        if recent_events.get('earnings'):
            earnings = recent_events['earnings']
            eps_surprise = earnings.get('eps_surprise_percent', 0)
            if abs(eps_surprise) > 3:
                reasons.append(
                    f"Earnings {'beat' if eps_surprise > 0 else 'missed'} "
                    f"by {abs(eps_surprise):.1f}%"
                )

        # Check for material 8-K filings
        if recent_events.get('8k_filings'):
            reasons.append(f"Filed {len(recent_events['8k_filings'])} material event(s)")

        # Check for news sentiment
        if recent_events.get('news'):
            news = recent_events['news']
            avg_sentiment = sum(n.get('sentiment', 0) for n in news) / len(news)
            if avg_sentiment > 0.3:
                reasons.append("Strong positive news sentiment")
            elif avg_sentiment < -0.3:
                reasons.append("Negative news sentiment")

        # Check for analyst actions
        if recent_events.get('analyst_upgrades'):
            reasons.append(f"Analyst upgrade(s): {recent_events['analyst_upgrades']}")

        if reasons:
            return f"{ticker} moved {price_change_percent:+.1f}% due to: {', '.join(reasons)}"
        else:
            return f"{ticker} moved {price_change_percent:+.1f}% (no clear catalyst identified)"


# Singleton instance
stock_analyzer = StockAnalyzer()
