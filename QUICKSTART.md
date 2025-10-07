# Quick Start Guide

**Bloomberg Terminal for the Everyman - Get Running in 10 Minutes**

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ installed
- Docker Desktop installed (for PostgreSQL + Redis)

## Step 1: Clone & Setup Environment (2 min)

```bash
cd Fintech-Tracker

# Copy and configure environment variables
# (API keys are already in .env from your setup)
cat .env
```

Your `.env` should have:
```
FINPREP_API_KEY=3j1RBgxesAt5Qic68ARvitKvbxdr5o6p
ALPHAVANTAGE_API_KEY=7TPNLET3G5Q5BOUB
MARKETAUX_API_KEY=PRcDaB8zIEJM9hnZ9kix1LrgoRz1skbzdpWl7sYr
```

## Step 2: Start Database (1 min)

```bash
# Start PostgreSQL + Redis
docker-compose up -d

# Verify they're running
docker ps
```

You should see:
- `fintech_db` on port 5432
- `fintech_redis` on port 6379

## Step 3: Setup Backend (3 min)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python -m app.main
```

Backend should be running on: **http://localhost:8000**

API docs available at: **http://localhost:8000/api/docs**

## Step 4: Setup Frontend (3 min)

Open a NEW terminal:

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend should be running on: **http://localhost:3000**

## Step 5: Verify Everything Works (1 min)

1. **Check Backend Health**:
   ```bash
   curl http://localhost:8000/api/health
   ```
   Should return: `{"status":"healthy",...}`

2. **Check API Docs**:
   Visit: http://localhost:8000/api/docs
   You should see interactive FastAPI documentation

3. **Check Frontend**:
   Visit: http://localhost:3000
   You should see the homepage with "Bloomberg Terminal for the Everyman"

## Single Command Startup

Once everything is set up, you can start the entire application with one command:

```bash
# Start everything (database + backend + frontend)
./start.sh

# Or using npm
npm start

# Or using make
make start
```

To stop:

```bash
./stop.sh
# or: npm run stop
# or: make stop
```

## You're Ready!

Now you can start building:

### Test the API Endpoints

```bash
# Get today's digest (mocked data for now)
curl http://localhost:8000/api/digest/today

# Get stock details
curl http://localhost:8000/api/stocks/NVDA

# Get earnings calendar
curl http://localhost:8000/api/events/earnings
```

### Next Steps

1. **Implement Data Fetching** (Week 1-2)
   - Edit `backend/app/services/data_fetcher.py`
   - Add SEC EDGAR integration
   - Add FRED API integration

2. **Build Attribution Engine** (Week 3-4)
   - Edit `backend/app/services/analyzer.py`
   - Test scoring on real stocks
   - Implement "why detector"

3. **Create Digest Page** (Week 5-6)
   - Create `frontend/src/app/digest/page.tsx`
   - Connect to `/api/digest/today` endpoint
   - Display recommendation card

## Common Issues

### Database Connection Error
```bash
# Make sure Docker is running
docker-compose up -d

# Check if PostgreSQL is healthy
docker-compose ps
```

### Frontend Won't Start
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

### Backend Import Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # You should see (venv) in your terminal

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Backend (8000)
lsof -ti:8000 | xargs kill -9

# Frontend (3000)
lsof -ti:3000 | xargs kill -9
```

## Stopping Everything

```bash
# Stop backend: Ctrl+C in backend terminal

# Stop frontend: Ctrl+C in frontend terminal

# Stop database
docker-compose down
```

## Development Workflow

```bash
# Always run these in order:
1. docker-compose up -d        # Start database
2. cd backend && python -m app.main   # Start backend
3. cd frontend && npm run dev  # Start frontend

# When you're done:
docker-compose down            # Stop database
```

## API Keys Used

Your current setup uses **FREE tier** API keys:

- **Financial Modeling Prep**: 250 calls/day (fundamentals, earnings)
- **Alpha Vantage**: 500 calls/day (backup fundamentals)
- **Marketaux**: 100 requests/day (news)

These are enough for MVP development. You'll hit rate limits only if you make excessive requests.

## Ready to Build?

Start with the data pipeline:
```bash
cd backend/app/services
# Edit data_fetcher.py and implement:
# - get_sec_filings()
# - get_macro_data()
```

Then test it:
```python
python
>>> from app.services.data_fetcher import data_fetcher
>>> data = data_fetcher.get_stock_price("NVDA")
>>> print(data)
```

Good luck!
