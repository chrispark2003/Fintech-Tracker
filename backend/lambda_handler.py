"""
AWS Lambda handler for FastAPI application
Uses Mangum adapter to run FastAPI on Lambda
"""

from mangum import Mangum
from app.main import app

# Lambda handler
handler = Mangum(app, lifespan="off")
