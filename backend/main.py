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

import logging

app = FastAPI(
    title="Smart Car Recommendation System API",
    version="1.0.0",
    description="Smart Car Recommendation System backend"
)


@app.on_event("startup")
def startup_event():
    """
    FastAPI startup event handler.
    Configures a logging filter to suppress Webpack HMR request logs from polluting the console.
    """
    class HMRFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            return ".hot-update.json" not in record.getMessage()
    
    logging.getLogger("uvicorn.access").addFilter(HMRFilter())


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
    Root endpoint for service verification. Returns API welcome message.
    """
    return {"message": "Backend is running!"}


@app.get("/health")
def health():
    """
    Health check endpoint to verify container status and connectivity.
    """
    return {"status": "OK", "healthy": True}


app.include_router(api_router, tags=["Recommendation & Explore"])