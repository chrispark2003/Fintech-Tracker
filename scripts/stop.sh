#!/bin/bash

# Fintech Tracker - Stop Script

echo " Stopping Fintech Tracker..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Stop Frontend
if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "  Stopping Frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        rm logs/frontend.pid
        echo "${GREEN} Frontend stopped${NC}"
    else
        echo "${RED}Frontend process not found${NC}"
        rm logs/frontend.pid
    fi
else
    echo "No frontend.pid file found"
fi

# Stop Backend
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo " Stopping Backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        rm logs/backend.pid
        echo "${GREEN} Backend stopped${NC}"
    else
        echo "${RED}Backend process not found${NC}"
        rm logs/backend.pid
    fi
else
    echo "No backend.pid file found"
fi

# Stop Database
echo " Stopping Database services..."
if command -v docker &> /dev/null && docker compose version &> /dev/null 2>&1; then
    docker compose down
elif command -v docker-compose &> /dev/null; then
    docker-compose down
fi
echo "${GREEN} Database services stopped${NC}"

echo ""
echo "════════════════════════════════════════════════════════════"
echo " ${GREEN}Fintech Tracker stopped successfully${NC}"
echo "════════════════════════════════════════════════════════════"
echo ""
