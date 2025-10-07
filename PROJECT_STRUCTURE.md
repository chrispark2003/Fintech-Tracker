# Fintech Tracker - Project Structure

**Bloomberg Terminal for the Everyman**

## Directory Structure

```
Fintech-Tracker/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry point
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py  # Health check endpoints
│   │   │       ├── stocks.py  # Stock data endpoints
│   │   │       ├── digest.py  # Daily digest (THE core feature)
│   │   │       └── events.py  # Market events (earnings, filings, macro)
│   │   ├── core/
│   │   │   ├── config.py      # Settings & environment variables
│   │   │   └── database.py    # Database connection & session
│   │   ├── models/
│   │   │   └── stock.py       # SQLAlchemy database models
│   │   ├── services/
│   │   │   ├── data_fetcher.py  # Fetch data from APIs (yfinance, FMP, etc.)
│   │   │   └── analyzer.py      # Stock analysis & scoring (YOUR MOAT)
│   │   └── utils/
│   ├── tests/                 # Unit tests
│   ├── scripts/               # Data ingestion & cron jobs
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # Next.js React frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout
│   │   │   ├── page.tsx       # Homepage
│   │   │   └── globals.css    # Global styles
│   │   ├── components/
│   │   │   ├── ui/            # Reusable UI components
│   │   │   └── features/
│   │   │       └── RecommendationCard.tsx  # Main recommendation display
│   │   ├── lib/
│   │   │   └── api.ts         # API client for backend
│   │   ├── hooks/             # Custom React hooks
│   │   └── types/             # TypeScript type definitions
│   ├── public/                # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── next.config.js
│
├── data/                      # Data storage (gitignored)
│   ├── raw/                   # Raw data from APIs
│   └── processed/             # Processed/cleaned data
│
├── docs/                      # Documentation
│
├── .env                       # Environment variables (API keys)
├── .gitignore
├── docker-compose.yml         # PostgreSQL + Redis for local development
└── README.md                  # Project roadmap
```

## Key Files & Their Purpose

### Backend Core Files

#### `backend/app/main.py`
- FastAPI application entry point
- Defines all API routes
- CORS configuration for frontend

#### `backend/app/core/config.py`
- Loads environment variables from `.env`
- API keys: FINPREP_API_KEY, MARKETAUX_API_KEY, etc.
- Database connection string

#### `backend/app/models/stock.py`
- Database schema definitions:
  - `stocks`: Stock metadata
  - `stock_prices`: OHLCV time-series data
  - `stock_fundamentals`: P/E, ROE, growth rates
  - `news`: News articles with sentiment
  - `sec_filings`: 8-K, 10-K, 10-Q filings
  - `recommendations`: Daily stock picks

#### `backend/app/services/data_fetcher.py`
- Fetches data from free APIs:
  - yfinance (prices)
  - Financial Modeling Prep (fundamentals, earnings)
  - Marketaux (news)
  - SEC EDGAR (filings)
  - FRED (macro data)

#### `backend/app/services/analyzer.py`  **YOUR COMPETITIVE MOAT**
- `calculate_technical_score()`: RSI, MACD, moving averages → 0-10 score
- `calculate_fundamental_score()`: P/E, ROE, growth → 0-10 score
- `calculate_catalyst_score()`: News, filings, earnings → 0-10 score
- `generate_recommendation()`: Combines scores → BUY/SELL/HOLD
- `detect_why()`: **Attribution engine** - links price moves to catalysts

### Frontend Core Files

#### `frontend/src/app/page.tsx`
- Homepage with value propositions
- Links to digest and stock pages

#### `frontend/src/components/features/RecommendationCard.tsx`
- Main UI component for displaying daily recommendation
- Shows: ticker, action, price targets, catalyst, reasoning

#### `frontend/src/lib/api.ts`
- TypeScript API client
- Type-safe endpoints for digest, stocks, events

### Configuration Files

#### `.env`
```
FINPREP_API_KEY=your_key_here
ALPHAVANTAGE_API_KEY=your_key_here
MARKETAUX_API_KEY=your_key_here
```

#### `docker-compose.yml`
- Spins up PostgreSQL + Redis locally
- Run: `docker-compose up -d`

## Running the Project

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL + Redis
docker-compose up -d

# Run backend
python -m app.main
# API docs: http://localhost:8000/api/docs
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Open: http://localhost:3000
```

## Next Steps to Build MVP

1. **Week 1-2: Data Pipeline**
   - Implement `data_fetcher.py` methods (SEC EDGAR, FRED)
   - Create database tables with Alembic migrations
   - Build daily cron job to ingest S&P 500 data

2. **Week 3-4: Screening Logic**
   - Implement `analyzer.py` scoring functions
   - Test on historical data
   - Identify top daily candidates

3. **Week 5-6: Digest Generation**
   - Complete `digest.py` endpoint
   - Generate daily recommendation
   - Track performance metrics

4. **Week 7-8: Frontend Polish**
   - Build digest page (`frontend/src/app/digest/page.tsx`)
   - Add charts (Recharts)
   - Mobile-responsive design

## Deployment

### Free Hosting Options

- **Frontend**: Vercel (auto-deploy from GitHub)
- **Backend**: Railway.app or Render (free tier)
- **Database**: Supabase (free PostgreSQL)
- **Cron Jobs**: GitHub Actions (free)

**Total cost: $0/month for MVP**

## Data Sources (All Free Tier)

-  **yfinance**: Price data
-  **Financial Modeling Prep**: Fundamentals (250 calls/day free)
-  **Finnhub**: News + sentiment (60 calls/min free)
-  **Marketaux**: News (100 requests/day free)
-  **SEC EDGAR**: Filings (unlimited free)
-  **FRED**: Macro data (unlimited free)

## Your Competitive Advantage

**Not the data sources** - everyone has access to yfinance and SEC filings.

**It's the attribution engine** (`analyzer.py`) that answers:
- WHY did NVDA move 5% today?
- Which stocks have strong catalysts + technical setups?
- What's THE ONE best opportunity right now?

This is your moat. Focus 80% of development here.
