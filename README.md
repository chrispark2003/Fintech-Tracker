# Fintech Investment Intelligence Platform - Roadmap

## Project Overview

### Vision
Build two foundational products that democratize market intelligence:
1. **Finance Product**: Aggregates and presents stock market news (IPOs, earnings, market-moving events) with actionable recommendations
2. **Real Estate Product**: Does the same for real estate (new listings, price changes, development news)

Both products solve the same core problem: **providing timely, actionable market intelligence for busy people who want to invest but lack time to keep up with fast-moving markets**.

### Core Problem Statement
"These worlds move fast, and I'm too busy to keep up with it"

### Success Metrics
- 20 minutes per day engagement time
- 2-3 confident investment decisions per month
- Information accessible to non-experts (between Bloomberg Terminal complexity and basic Apple stock notifications)

---

## Phase 1: Finance Product MVP (Equities + ETFs Only)

### Timeline: 8-12 weeks (Side project during final semester at Georgia Tech)

### Budget: $0-15/month
- Leverage student credits (AWS Educate, GitHub Student Pack, Azure for Students)
- Use free API tiers initially
- Scale spending only when validated

### Target User
Initial: Personal use only
Future: Non-expert investors who want confident, digestible recommendations

### Product Scope

#### Daily Deliverable (10 minutes)
- Market overnight moves and drivers
- Today's key events (earnings, Fed speeches, data releases)
- **ONE primary recommendation** across all asset classes (equities/ETFs for MVP)
  - Full reasoning: catalyst, timing, risk/reward, position sizing
- 2-3 "watch list" items
- Portfolio alerts (if tracking holdings)

#### Weekly Deliverable (30 minutes, Sunday)
- Comprehensive market review
- 1-3 high-conviction recommendations
- Asset allocation guidance
- Macro themes driving opportunities
- Educational component

---

## Technical Architecture

### Core Philosophy
**"AI assists my analysis, I make the decisions"**

```
┌──────────────────────────────────────────────┐
│         YOUR DETERMINISTIC LOGIC             │
│  (Screening, Scoring, Ranking, Risk Mgmt)    │
│         ← This makes the decisions           │
└──────────────┬───────────────────────────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
┌───▼────────────┐    ┌──────────▼──────────┐
│  AI HELPERS    │    │   AI EXPLAINER      │
│                │    │                     │
│ - Summarize    │    │ "You ranked NVDA    │
│   news         │    │  #1 because..."     │
│ - Extract      │    │                     │
│   earnings     │    │ [Takes YOUR data    │
│   data         │    │  + reasoning,       │
│ - Sentiment    │    │  makes it readable] │
│   scores       │    │                     │
└────────────────┘    └─────────────────────┘
```

### System Architecture

```
┌─────────────────┐
│  Data Ingestion │ (daily cron job)
│  - Price data   │
│  - Fundamentals │
│  - News/events  │
└────────┬────────┘
         │
┌────────▼────────┐
│   Analysis      │
│   Pipeline      │
│  - Screen       │
│  - Score        │
│  - Rank         │
└────────┬────────┘
         │
┌────────▼────────┐
│ Recommendation  │
│    Engine       │
│ - Select top 1  │
│ - Generate      │
│   reasoning     │
└────────┬────────┘
         │
┌────────▼────────┐
│   Delivery      │
│ - Email/Slack   │
│ - Dashboard     │
└─────────────────┘
```

### Tech Stack

#### Data Layer
- **yfinance** (Python) - Free Yahoo Finance data
- **Alpha Vantage** - Free tier for fundamentals, news sentiment (500 calls/day)
- **Financial Modeling Prep API** - $0-29/mo, excellent fundamentals + earnings
- **Marketaux** - Free tier for news (100 requests/day, real-time)
- **EDGAR API** (SEC) - Free for insider trading, 10-Ks, 8-Ks

#### Backend (Python)
- **Pandas** - Data manipulation
- **NumPy** - Calculations
- **pandas-ta** - Technical analysis indicators (easier than TA-Lib for MVP)
- **QuantStats** - Performance analytics and risk metrics
- **PyPortfolioOpt** - Portfolio optimization and risk management
- **FastAPI** - Lightweight API framework (if building web interface)
- **Celery + Redis** - Scheduled tasks for daily data pulls

#### Database
- **PostgreSQL** - Time-series data, historical prices, fundamentals
- **SQLite** - Alternative for truly personal use only
- **TimescaleDB** (Postgres extension) - For scaling time-series data

#### AI Components (Optional for MVP)
- **OpenAI API** or **Anthropic API** - $5-20/mo for summarization ($0.50-2.00 per 1M tokens)
- **FinBERT** (free, open source) - Financial sentiment analysis
- **Llama 3.1 8B** - Free local alternative (slower)

#### Frontend (Personal Use)
- **Email digest** - HTML emails via SendGrid/Mailgun (free tier)
- **Streamlit** dashboard - Python-native, rapid prototyping
- **Notion API** - Auto-populate daily pages
- Or headless: Slack/Discord notifications

#### Hosting
- **AWS Free Tier** (12 months) - EC2 t2.micro, RDS db.t2.micro
- **DigitalOcean** - $5/mo droplet
- **Local machine** - $0 (totally viable for personal use)

---

## Development Roadmap

### Week 1-2: Data Pipeline
**Goal**: Reliable data ingestion

- [ ] Set up development environment (Python 3.10+, PostgreSQL)
- [ ] Register for API keys (yfinance, Alpha Vantage, Marketaux, FMP)
- [ ] Pull daily price data for S&P 500
- [ ] Store in database with proper schema
- [ ] Calculate basic technical indicators (RSI, MACD, volume)
- [ ] Verify data quality and consistency

**Deliverable**: Script that fetches and stores daily market data

### Week 3-4: Screening Logic
**Goal**: Identify interesting candidates

- [ ] Define "interesting" criteria
  - Momentum + value combination
  - Unusual volume patterns
  - Technical breakouts
  - Fundamental quality thresholds
- [ ] Implement screening filters
- [ ] Output top 10-20 candidates daily
- [ ] Manual review to validate quality

**Deliverable**: Daily list of candidate stocks with basic metrics

### Week 5-6: Scoring & Ranking System
**Goal**: Systematically rank opportunities

- [ ] Build multi-factor scoring model
  - Technical score (0-10): momentum, trend strength, volume
  - Fundamental score (0-10): valuation, growth, profitability
  - Catalyst score (0-10): news events, earnings, developments
- [ ] Define weighting system (e.g., 40% technical, 40% fundamental, 20% catalyst)
- [ ] Backtest against historical data (1-5 years)
- [ ] Refine scoring based on backtest results
- [ ] Select #1 recommendation daily

**Deliverable**: Ranked list with top recommendation identified

### Week 7-8: Risk Management & Narrative Generation
**Goal**: Complete recommendation package

- [ ] Calculate position sizing based on portfolio risk
- [ ] Set stop-loss levels
- [ ] Estimate risk/reward ratios
- [ ] Build narrative generation system
  - Template-based explanations
  - Optional: LLM integration for natural language
- [ ] Format daily email/digest
- [ ] Set up automated delivery (SendGrid/Mailgun)

**Deliverable**: Complete daily recommendation delivered via email

### Week 9-12: Personal Use & Iteration
**Goal**: Validate usefulness and refine

- [ ] Use recommendations yourself for paper trading or small positions
- [ ] Track performance of recommendations
- [ ] Identify gaps in analysis
- [ ] Refine scoring weights based on results
- [ ] Add missing data sources or indicators
- [ ] Improve narrative quality
- [ ] Optimize for 20-minute daily engagement

**Deliverable**: Production-ready personal tool with tracked performance

---

## Financial Analysis Implementation

### Use Libraries For (Don't Reinvent the Wheel)

#### Technical Indicators
```python
import pandas_ta as ta

# RSI, MACD, Bollinger Bands, Moving Averages
df.ta.rsi(length=14, append=True)
df.ta.macd(append=True)
df.ta.bbands(append=True)
```

**Libraries**:
- **pandas-ta** - Easiest to start, 130+ indicators
- **TA-Lib** - Industry standard, migrate here if you need performance

#### Fundamental Ratios
```python
import yfinance as yf

ticker = yf.Ticker("AAPL")
pe_ratio = ticker.info['forwardPE']
roe = ticker.info.get('returnOnEquity', 0)
```

**APIs**:
- **yfinance** - Basic ratios
- **Financial Modeling Prep** - More comprehensive, better quality

#### Risk Metrics
```python
import quantstats as qs

sharpe = qs.stats.sharpe(returns)
max_dd = qs.stats.max_drawdown(returns)
```

**Libraries**:
- **QuantStats** - Performance analytics
- **PyPortfolioOpt** - Portfolio optimization
- **empyrical** - Additional risk metrics

#### Backtesting
```python
import backtrader as bt

class MyStrategy(bt.Strategy):
    def next(self):
        if condition:
            self.buy()
```

**Libraries**:
- **Backtrader** - Full-featured, industry standard
- **Vectorbt** - Faster, more modern

### Build From Scratch (Your Competitive Advantage)

- **Custom scoring system** - How you combine signals
- **Screening logic** - What makes a stock "interesting" to you
- **Recommendation selection** - How you pick #1 from candidates
- **Narrative generation** - Your product's voice
- **Integration & orchestration** - Your unique architecture

---

## AI Integration Strategy

### ✅ Good Uses of AI/LLMs

1. **Data Processing & Extraction**
   - Parse earnings call transcripts
   - Summarize SEC filings
   - News summarization (10 articles → coherent summary)
   - Entity extraction from unstructured text

2. **Narrative Generation** (Explanation, not Decision)
   - Turn quantitative analysis into readable explanations
   - "NVDA scored 8.5/10 because: revenue growth +40% QoQ..."
   - You make decision, AI explains your logic

3. **Anomaly Detection** (ML, not LLMs)
   - Flag unusual patterns (volume spikes, correlation breaks)
   - Alert you to investigate, doesn't tell you what to do

4. **Sentiment Analysis**
   - Analyze social media, news sentiment at scale
   - Classify as positive/negative/neutral
   - Track sentiment trends

5. **Natural Language Interface** (Future)
   - "Show me tech stocks with earnings this week"
   - Query your data conversationally

### ❌ Bad Uses of AI/LLMs

1. **Final Investment Recommendations** - No accountability, hallucination risk
2. **Quantitative Scoring/Ranking** - LLMs can't do math reliably
3. **Risk Assessment** - Needs precision, not approximation
4. **Backtesting** - Requires auditable calculations

### Example: Daily Recommendation Flow

1. **Data collection** (Traditional code) - Pull prices, fundamentals, news
2. **Screening** (Your logic) - Filter S&P 500 to 50 candidates
3. **AI helper** (LLM) - Summarize news for each candidate
4. **Scoring** (Your logic) - Technical + Fundamental + Catalyst scores
5. **Risk assessment** (Your logic) - Position size, stop-loss, risk/reward
6. **Selection** (Your logic) - Pick top-ranked stock
7. **Narrative** (LLM) - Make your decision readable

**The LLM makes it readable. You made the actual decision.**

---

## Learning Path

### Phase 1: Understand the Tools (Week 1-2)

1. Install and experiment:
```bash
pip install yfinance pandas-ta quantstats pypfopt
```

2. Try basic examples:
   - Pull stock data with yfinance
   - Calculate RSI with pandas-ta
   - Compute Sharpe ratio with quantstats

3. Read library documentation

### Phase 2: Learn Financial Concepts (Weeks 3-4)

**You don't need an MBA, just working knowledge:**

- **Technical Analysis basics**: RSI, MACD, moving averages (Investopedia)
- **Fundamental Analysis basics**: P/E, P/B, ROE, debt-to-equity
- **Resources**:
  - Investopedia articles (free, searchable)
  - "Technical Analysis Explained" by Martin Pring (skim relevant chapters)
  - Company 10-Ks for fundamentals

**Goal**: Understand what indicators mean, when to use them

### Phase 3: Build & Iterate (Weeks 5+)

- Implement one indicator at a time
- Test on historical data
- See what correlates with good performance
- Build intuition through experimentation

**You'll learn more by building than by studying theory.**

---

## Cost Breakdown

### MVP Monthly Costs

#### Minimum Viable ($0/month)
- Run locally on laptop
- Free API tiers only (yfinance, Alpha Vantage free, Marketaux free)
- SQLite database
- Email via Gmail SMTP
- Manual trigger

**Limitations**: Rate limits, tied to personal machine, less reliable

#### Recommended MVP ($0-15/month)
- **Data & APIs**: $0-29/mo
  - yfinance: Free
  - Alpha Vantage: Free (500 calls/day)
  - Financial Modeling Prep: $0-29/mo (free tier: 250 calls/day)
  - Marketaux: Free (100 requests/day)
- **Hosting**: $0-10/mo
  - AWS Free Tier (12 months) or local: $0
  - DigitalOcean droplet: $5/mo
- **Database**: $0 (included in free tier or local)
- **Email**: $0 (SendGrid: 100/day free, Mailgun: 5000 free for 3 months)
- **AI (optional)**: $0-20/mo
  - OpenAI/Anthropic APIs: $5-20/mo
  - Or use free local models: $0

**Total**: $0-15/mo realistically for personal use

### Scaling Costs (Future)

**100 users**: ~$100-200/mo
**1,000 users**: ~$400-1,000/mo
**10,000 users**: ~$2-5K/mo (but you'd be charging by then)

---

## Phase 2: Expansion Strategy

### After MVP Validated (Post-Graduation)

#### Path 1: Add Asset Classes to Finance Product
1. **Crypto** (3-6 months)
   - CoinGecko, Messari APIs
   - On-chain metrics
   - Similar screening/scoring approach

2. **Options** (3-6 months)
   - CBOE data, options flow
   - Greeks, implied volatility
   - More complex risk management

3. **Bonds/Fixed Income** (3-6 months)
   - Treasury data, corporate bonds
   - Yield curves, credit spreads

#### Path 2: Real Estate Product (5-7 years timeline)
**Initial focus: Atlanta market**

**Data sources**:
- Zillow/Redfin APIs or scraping
- Public records (sales, tax assessments, permits)
- Local news (developments, zoning)
- Economic indicators (Atlanta Fed, employment, migration)
- Neighborhood data (crime, schools, new businesses)

**Structure**:
- Weekly report: Market overview, notable listings, price movements, development news
- Daily digest: Triggered by significant events only

**Similar architecture to finance product**:
- Data ingestion → Analysis → Scoring → Recommendation → Delivery
- Real estate moves slower, so less frequent updates

#### Path 3: Multi-User Product
1. User accounts and profiles
2. Personalization (risk tolerance, preferences, portfolio tracking)
3. Performance tracking per user
4. Subscription model ($10-50/mo per user)
5. Compliance and disclaimers (not financial advice)

---

## Key Principles & Reminders

### Product Philosophy
- **Depth over breadth** - Master one thing before expanding
- **Build for yourself first** - If you wouldn't use it, it's not good enough
- **Lower barriers to access** - Non-experts should understand it
- **Digestible, not overwhelming** - One recommendation beats ten mediocre ones

### Technical Philosophy
- **Don't reinvent the wheel** - Use proven libraries for calculations
- **Your secret sauce** - Custom scoring and selection logic
- **AI assists, you decide** - Never let AI make final investment decisions
- **Start simple, scale smart** - Local/free first, cloud when needed

### Development Philosophy
- **Ship and iterate** - Perfect is the enemy of done
- **Track performance** - Document recommendation results from day one
- **Stay skeptical** - If you wouldn't invest, the recommendation isn't good enough
- **Learn by building** - Code first, study theory as needed

---

## Success Criteria

### MVP Success (3 months)
- [ ] Daily recommendations delivered automatically
- [ ] 20-minute engagement time achieved
- [ ] You make 2-3 confident decisions per month based on it
- [ ] Performance tracking shows positive results (paper trading or real)
- [ ] System runs reliably without daily maintenance

### Product-Market Fit (Post-Graduation)
- [ ] 10+ friends/classmates using it and providing feedback
- [ ] Recommendations beating S&P 500 index over 6+ months
- [ ] Users spending less time researching, more confidence in decisions
- [ ] Feature requests indicating real value
- [ ] Willingness to pay for the service

### Long-Term Vision (2-5 years)
- [ ] Finance product covers all major asset classes
- [ ] Real estate product launched in Atlanta
- [ ] Both products share infrastructure
- [ ] Monetization strategy validated
- [ ] Community of users benefiting from democratized market intelligence

---

## Next Steps (Start This Week)

1. **Set up development environment**
   - Install Python 3.10+, PostgreSQL
   - Create GitHub repo
   - Get API keys

2. **Build simplest possible data pipeline**
   - Fetch data for 10 stocks
   - Store in database
   - Calculate one indicator (RSI)

3. **Manual analysis**
   - Look at the data
   - Make one recommendation yourself
   - Document your reasoning

4. **Iterate toward automation**
   - Codify your reasoning
   - Test on historical data
   - Build confidence in your approach

**The best time to start was yesterday. The second best time is now.**

---

## Resources

### Documentation
- pandas-ta: https://github.com/twopirllc/pandas-ta
- yfinance: https://github.com/ranaroussi/yfinance
- QuantStats: https://github.com/ranaroussi/quantstats
- PyPortfolioOpt: https://pyportfolioopt.readthedocs.io/
- Backtrader: https://www.backtrader.com/

### Learning
- Investopedia (free, searchable financial concepts)
- "A Random Walk Down Wall Street" by Burton Malkiel (context)
- "Technical Analysis Explained" by Martin Pring (reference)
- r/algotrading subreddit (community)

### Student Resources
- AWS Educate: $100+ credits
- GitHub Student Pack: DigitalOcean credits, domain name, etc.
- Azure for Students: $100 credit

---

## Notes

- This is a **side project** during final semester at Georgia Tech CS
- Potential to become **post-graduation focus** if validated
- Built on philosophy of **minimizing barriers to access**
- Personal use first, then expand to others
- **Document everything** - future marketing material and proof of concept

---

**Last Updated**: October 2025
**Status**: Planning → Development
**Current Phase**: Pre-MVP, Setting up development environment
