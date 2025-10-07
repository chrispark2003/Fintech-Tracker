# Fintech Investment Intelligence Platform - Roadmap

## Project Overview

### Vision
**"Bloomberg Terminal for the Everyman"**

Democratize institutional-grade market intelligence by aggregating and presenting stock market news (IPOs, earnings, market-moving events) with actionable, digestible recommendations.

**Core problem**: Providing timely, actionable market intelligence for busy people who want to invest but lack time to keep up with fast-moving markets.

### The Opportunity
Bloomberg Terminal costs $24,000/year and requires professional training. This platform delivers:
- **Institutional-grade intelligence** at retail pricing ($0-50/month)
- **20 minutes per day** vs hours of Bloomberg analysis
- **Digestible insights** vs overwhelming data terminals
- **Non-expert accessible** vs finance professional only

### Core Problem Statement
- "These worlds move fast, and I'm too busy to keep up with it"
- "**Solution: The everyman's bloomberg terminal**"

### Success Metrics
- 20 minutes per day engagement time
- 2-3 confident investment decisions per month
- Information accessible to non-experts (between Bloomberg Terminal complexity and basic Apple stock notifications)

### Competitive Advantage
**Not the data sources - it's the intelligence layer built on top of free/cheap data.**
- Bloomberg's weakness = Our opportunity: Price, complexity, time required, accessibility
- Our moat = Attribution engine that answers "WHY did this stock move?" using publicly available data

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

#### Data Layer (MVP: 100% Free Tier - $0/month)

**Critical Data Sources (All Free):**
- **yfinance** - FREE, unlimited EOD prices, basic fundamentals
- **Financial Modeling Prep** - FREE tier: 250 calls/day (fundamentals, earnings, analyst ratings)
  - https://financialmodelingprep.com/developer/docs/
- **SEC EDGAR API** - FREE, unlimited official filings (8-K, 10-K, 10-Q, Form 4)
  - https://www.sec.gov/edgar/sec-api-documentation
- **Finnhub** - FREE tier: 60 calls/min (news, earnings calendar, sentiment)
  - https://finnhub.io/
- **Marketaux** - FREE tier: 100 requests/day (real-time news)
  - https://www.marketaux.com/documentation
- **FRED API** - FREE, unlimited (CPI, unemployment, Fed rates, macro data)
  - https://fred.stlouisfed.org/docs/api/fred/
- **FINRA** - FREE short interest data (twice monthly)
- **Reddit/StockTwits APIs** - FREE social sentiment

**Optional Upgrades (Phase 2):**
- **Financial Modeling Prep Pro**: $29/mo (higher rate limits)
- **Polygon.io**: $29-200/mo (real-time prices, options data)
- **Alpha Vantage**: Backup for fundamentals (500 calls/day free)

**Deprioritized (Expensive, Low ROI for MVP):**
-  Professional options flow: $200+/mo
-  Real-time tick data: $500-5000/mo
-  Alternative data (satellite, credit cards): $$$$$
-  Bloomberg/FactSet terminals: $24k-50k/year

**Data Philosophy:**
- Start with 100% free tier - validates product before spending on data
- 80% of Bloomberg's value comes from data that's free or nearly free
- Competitive advantage is intelligence layer, not raw data access
- Upgrade only when revenue justifies cost
   

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
**Goal**: Reliable data ingestion from free sources

**Priority 1: Core Data (100% Free)**
- [x] Set up development environment (Python 3.10+, PostgreSQL)
- [x] Register for free API keys:
  - [x] Financial Modeling Prep (250 calls/day free)
  - [x] Finnhub (60 calls/min free) - Using Marketaux instead
  - [x] Marketaux (100 requests/day free)
  - [x] FRED API (unlimited free) - Key not needed, public access
  - [x] SEC EDGAR (unlimited free) - No key needed, public API
- [ ] Build data ingestion pipeline:
  - [ ] yfinance: Daily EOD prices for S&P 500
  - [ ] FMP: Fundamentals (P/E, EPS, revenue growth)
  - [ ] SEC EDGAR: 8-K filings (material events)
  - [ ] Finnhub: News + earnings calendar
  - [ ] FRED: Macro indicators (CPI, unemployment)
- [ ] Store in PostgreSQL with proper schema
- [ ] Calculate basic technical indicators (RSI, MACD, volume)
- [ ] Verify data quality and cross-validate (yfinance vs FMP)

**Priority 2: Attribution Engine Foundation**
- [ ] Link price movements to events (8-K filings, earnings, news)
- [ ] Build "why detector": If stock moves >3%, check for catalyst within 48h

**Deliverable**: Script that fetches free data and identifies basic catalysts

**Key Insight**: You can build 80% of Bloomberg's value with $0 in data costs

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

### Good Uses of AI/LLMs

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

### Bad Uses of AI/LLMs

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

#### Recommended MVP ($0/month - Start Here)
**All free tier, validates product before spending:**
- **Data & APIs**: $0
  - yfinance: Free unlimited EOD prices
  - Financial Modeling Prep: Free tier (250 calls/day)
  - Finnhub: Free tier (60 calls/min)
  - Marketaux: Free (100 requests/day)
  - SEC EDGAR: Free unlimited
  - FRED API: Free unlimited
  - Reddit/StockTwits: Free
- **Hosting**: $0
  - Run locally on laptop OR AWS Free Tier (12 months)
- **Database**: $0
  - PostgreSQL locally OR AWS RDS free tier
- **Email**: $0
  - SendGrid: 100/day free OR Gmail SMTP
- **AI (optional)**: $0
  - Use free local models (Llama) OR minimal OpenAI usage ($1-5/mo)

**Total: $0/month**

**Limitations**: Rate limits (but sufficient for S&P 500 daily), tied to personal machine (but fine for MVP)

**Key Point**: You don't need to spend money to validate the product. Free tier covers 100% of MVP functionality.

### Scaling Costs (Revenue-Driven)

**Phase 1: $0 MRR (Personal use)**
- Cost: $0/month
- Use 100% free tier

**Phase 2: $50 MRR (10 users × $5/mo)**
- Cost: $29/mo
- Upgrade: FMP Pro for better rate limits

**Phase 3: $500 MRR (50 users × $10/mo)**
- Cost: ~$100-200/mo
- Upgrade: Polygon.io for real-time data
- Hosting: DigitalOcean/AWS paid tier

**Phase 4: $2000+ MRR (200+ users × $10/mo)**
- Cost: ~$400-1000/mo
- Add: Options flow data, premium news feeds
- Profit margin: 50-80%

**Key principle**: Spend only when revenue justifies it. Start at $0, scale spending as revenue grows.

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

#### Path 2: Multi-User Product
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
- [ ] Finance product covers all major asset classes (equities, ETFs, options, crypto, bonds)
- [ ] Multi-user platform with personalization
- [ ] Monetization strategy validated ($10-50/mo subscriptions)
- [ ] Community of users benefiting from democratized market intelligence
- [ ] Proven track record of recommendations beating S&P 500

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

## Financial Data Sources for Real-Time Market Insight

This document catalogs APIs, feeds, and data sources you can use to understand **why the stock market behaves a certain way** at any given time — from fundamentals and filings to alternative signals and sentiment.

---

### Core Market & Reference Data

These are the backbone of any financial data system: prices, fundamentals, filings, and macro data.

#### **1. Historical & Intraday Prices**
- **[yfinance](https://github.com/ranaroussi/yfinance)**
  - Free, easy-to-use for daily or intraday OHLCV data.
  - **Pull:** OHLCV, splits, dividends, ticker metadata.
  - **Use:** End-of-day updates (daily) or intraday (1–5m).
- **[Polygon.io](https://polygon.io/)**
  - Tick-level trades, quotes, and WebSocket for real-time data.
  - **Pull:** Tick trades, NBBO, aggregated bars.
  - **Use:** Real-time or backfills via REST.

#### **2. Exchange & Consolidated Feeds**
- **[IEX Cloud](https://iexcloud.io/)** / **IEX Exchange**
  - Consolidated quotes, historical prices, and fundamentals.
  - Cost-effective alternative for real-time data.

#### **3. Fundamentals & Financial Statements**
- **[Financial Modeling Prep (FMP)](https://financialmodelingprep.com/developer/docs/)**
  - Income, balance sheet, cash flow, key ratios, earnings, and analyst data.
  - Great free tier; JSON endpoints.
- **[Alpha Vantage](https://www.alphavantage.co/)**
  - Fundamentals and technical indicators.
  - Free but with strict rate limits.

#### **4. SEC Filings**
- **[EDGAR API](https://www.sec.gov/edgar/sec-api-documentation)** / [sec-api.io](https://sec-api.io/)
  - Machine-readable filings: 10-K, 10-Q, 8-K, Form 4.
  - **Pull:** 8-K (events), Form 4 (insiders), S-1 (IPOs).

#### **5. Macro & Economic Indicators**
- **[FRED API](https://fred.stlouisfed.org/docs/api/fred/)**
  - Unemployment, CPI, GDP, interest rates, etc.
  - Use to correlate macro conditions with market movements.

---

### News & Real-Time Event / Sentiment Data

News and sentiment are often the *earliest indicators* of price movement.

#### **1. Market News APIs**
- **[Finnhub](https://finnhub.io/)**
  - News, earnings, transcripts, analyst ratings, sentiment.
  - **Pull:** News headlines, sentiment, earnings calendars.
- **[Marketaux](https://www.marketaux.com/)** / **[NewsAPI](https://newsapi.org/)** / **Benzinga**
  - Marketaux and NewsAPI are low-cost broad feeds.
  - Benzinga offers faster, premium financial headlines.

#### **2. Earnings Call Transcripts**
- **Sources:** Finnhub, Seeking Alpha, FactSet, Refinitiv.
  - Analyze management tone and surprises using FinBERT or LLMs.

#### **3. Social Sentiment**
- **[StockTwits API](https://api.stocktwits.com/developers)**
- **Reddit (via [Pushshift](https://github.com/pushshift/api))**
- **Twitter/X API**
  - **Pull:** Message volumes, trending tickers, bullish/bearish sentiment.

#### **4. Analyst & Brokerage Research**
- **Refinitiv**, **FactSet**, **AlphaSense** (paid)
  - Track analyst upgrades/downgrades and price target changes.

---

### Market Microstructure & Flow Data

Short-term market movements often stem from order pressure, options activity, and fund flows.

#### **1. Options Flow**
- **[ORATS](https://orats.com/)** / **Polygon** / **Tradier** / **LiveVol**
  - Capture large options trades or sweeps as early signals of sentiment.

#### **2. ETF Flows & Holdings**
- **iShares / Vanguard APIs**
  - Daily holdings and inflows/outflows; track sector pressure.

#### **3. Short Interest**
- **[FINRA Short Interest](https://www.finra.org/filing-reporting/regulatory-filings/short-interest)**
  - Monitor T+1 reports and borrow rates for squeeze potential.

#### **4. Order Book / Level 2 Data**
- **Polygon / Direct Exchange Feeds**
  - Analyze liquidity depth and order book imbalance.

---

### Alternative & Contextual Data

"Alternative data" offers insight into underlying **economic behavior** beyond traditional finance metrics.

#### **1. Web & App Traffic**
- **SimilarWeb**, **App Annie**, **Google Play / App Store**
  - Track engagement trends as early indicators of growth.

#### **2. Job Postings & Hiring**
- **LinkedIn**, **Indeed**, **Glassdoor APIs**
  - Hiring slowdowns or spikes hint at company growth cycles.

#### **3. Consumer Spending**
- **Earnest Research**, **Yodlee**, **Neilsen**
  - Transaction-level data for consumer-driven companies.

#### **4. Satellite / Foot Traffic**
- **Orbital Insight**, **SafeGraph**, **Placer.ai**
  - Retail and logistics movement from geospatial data.

#### **5. Google Trends**
- Free, fast proxy for public attention and brand interest.

---

### Scraping & Crawling Targets

> **Note:** Always follow `robots.txt` and Terms of Service; avoid paywalled or proprietary content.

- **Company IR pages:** detect new press releases or filings.
- **RSS feeds:** Reuters, CNBC, Bloomberg, WSJ.
- **Earnings transcripts:** Seeking Alpha, Motley Fool.
- **Reddit/StockTwits:** track post spikes for retail sentiment.

---

### Data Ingestion & Processing Stack

**Recommended lightweight MVP stack:**

| Layer | Tool | Purpose |
|-------|------|----------|
| **Scheduling** | Cron / Celery | Regular pulls (hourly/daily) |
| **Storage** | PostgreSQL / TimescaleDB | Timeseries + metadata |
| **Normalization** | Pydantic models | Unify schemas across APIs |
| **Sentiment** | FinBERT / GPT-4o-mini | Summarize or score text |
| **Backups** | Cross-validation | Validate prices from multiple APIs |

---

### What to Collect Each Run

| Category | Key Data Points |
|-----------|----------------|
| Price & Volume | OHLCV (daily/intraday) |
| Technical Indicators | RSI, MACD, MAs, volume spikes |
| Earnings | EPS beats/misses, guidance |
| SEC Filings | 8-K, 10-K, Form 4 |
| News & Sentiment | Headlines, tone, clustering |
| Options Flow | Unusual OTM buys, open interest |
| Analyst Actions | Rating & target changes |
| ETF Flows | Inflows/outflows |
| Short Interest | Short volume, borrow rates |
| Macro | CPI, Fed decisions, unemployment |
| Social | Reddit/StockTwits/Twitter activity |
| Company Ops | Job listings, launches, closures |

---

### Implementation Tips

- **Normalize timestamps** → all UTC, nearest minute.
- **Classify latency tiers** → (real-time, near-real-time, daily, quarterly).
- **Add confidence scoring** → cross-source confirmation boosts reliability.
- **Cache expensive data** → fundamentals & filings rarely change.
- **Stay compliant** → respect API licensing & TOS.

---

### MVP-Ready Stack (High ROI, $0 Cost)

| Category | Tool | Cost |
|-----------|------|------|
| **Price Data** | yfinance | FREE |
| **Fundamentals** | Financial Modeling Prep (free tier) | FREE |
| **News/Sentiment** | Finnhub + Marketaux (free tiers) | FREE |
| **Filings** | SEC EDGAR API | FREE |
| **Macro Data** | FRED API | FREE |
| **Social Sentiment** | Reddit + StockTwits APIs | FREE |
| **Short Interest** | FINRA | FREE |

**Total MVP Data Cost: $0/month**

This stack provides 80% of Bloomberg Terminal's core functionality using only free data sources.

---

### Data Collection Next Steps

Choose one to implement next:

1. **API Integration Plan**
   Endpoints, rate limits, and cost estimates for a ready-to-build pipeline.
2. **Example ETL Script**
   Pulls price + fundamentals + news for 10 tickers → PostgreSQL schema.
3. **"Why" Attribution Logic**
   SQL schema + pseudocode to link price movements to catalysts (news, filings, options flow).

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
