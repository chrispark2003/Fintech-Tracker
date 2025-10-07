#!/bin/bash

# Fintech Tracker - One-Command Startup Script
# Bloomberg Terminal for the Everyman

set -e  # Exit on error

echo " Starting Fintech Tracker..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo " Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Step 1: Start Database
echo "${YELLOW} Starting PostgreSQL + Redis...${NC}"
# Try new docker compose command first, fallback to old
if command -v docker &> /dev/null && docker compose version &> /dev/null 2>&1; then
    docker compose up -d
elif command -v docker-compose &> /dev/null; then
    docker-compose up -d
else
    echo "Error: Neither 'docker compose' nor 'docker-compose' found."
    echo "Please install Docker Desktop: https://www.docker.com/products/docker-desktop/"
    exit 1
fi
echo "${GREEN} Database services started${NC}"
echo ""

# Wait for database to be ready
echo " Waiting for database to be ready..."
sleep 3

# Step 2: Check if backend venv exists
if [ ! -d "backend/venv" ]; then
    echo "${YELLOW} Creating Python virtual environment...${NC}"
    cd backend

    # Try to find compatible Python version (3.10 or 3.11)
    if command -v python3.10 &> /dev/null; then
        PYTHON_CMD=python3.10
    elif command -v python3.11 &> /dev/null; then
        PYTHON_CMD=python3.11
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    else
        echo "Error: Python 3.10+ not found. Install with: brew install python@3.10"
        exit 1
    fi

    echo "Using $PYTHON_CMD"
    $PYTHON_CMD -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt > /dev/null 2>&1
    cd ..
    echo "${GREEN} Backend dependencies installed${NC}"
else
    echo "${GREEN} Backend virtual environment exists${NC}"
fi
echo ""

# Step 3: Check if frontend node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "${YELLOW} Installing frontend dependencies...${NC}"
    cd frontend
    npm install > /dev/null 2>&1
    cd ..
    echo "${GREEN} Frontend dependencies installed${NC}"
else
    echo "${GREEN} Frontend dependencies installed${NC}"
fi
echo ""

# Step 4: Start Backend (in background)
echo "${YELLOW} Starting Backend API...${NC}"
cd backend
source venv/bin/activate
nohup python -m app.main > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..
echo "${GREEN} Backend started (PID: $BACKEND_PID)${NC}"
echo "   Logs: tail -f logs/backend.log"
echo ""

# Wait for backend to start
echo " Waiting for backend to start..."
sleep 3

# Step 5: Start Frontend (in background)
echo "${YELLOW}  Starting Frontend...${NC}"
cd frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..
echo "${GREEN} Frontend started (PID: $FRONTEND_PID)${NC}"
echo "   Logs: tail -f logs/frontend.log"
echo ""

# Wait for frontend to start
echo " Waiting for frontend to start..."
sleep 5

echo ""
echo "════════════════════════════════════════════════════════════"
echo " ${GREEN}Fintech Tracker is now running!${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
echo " Frontend:  http://localhost:3000"
echo " Backend:   http://localhost:8000"
echo " API Docs:  http://localhost:8000/api/docs"
echo ""
echo " Database:  PostgreSQL on localhost:5432"
echo " Redis:     localhost:6379"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "To stop everything, run: ${YELLOW}./scripts/stop.sh${NC}"
echo "To view logs:"
echo "  - Backend:  tail -f logs/backend.log"
echo "  - Frontend: tail -f logs/frontend.log"
echo ""
