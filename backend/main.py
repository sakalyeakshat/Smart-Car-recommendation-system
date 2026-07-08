"""
Main FastAPI application entry point.
Sets up the API application, CORS middleware, and includes all routers.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.recommend import router as api_router

app = FastAPI(
    title="Smart Car Recommendation System API",
    version="1.0.0",
    description="Smart Car Recommendation System backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """
    Root endpoint to verify the backend is responsive.
    """
    return {"message": "Backend is running!"}


@app.get("/health")
def health():
    """
    Health check endpoint for Docker container status monitoring.
    """
    return {"status": "OK", "healthy": True}


app.include_router(api_router, tags=["Recommendation & Explore"])