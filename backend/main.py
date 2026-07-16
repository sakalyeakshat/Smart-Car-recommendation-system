"""FastAPI application entry point that sets up CORS and registers the recommendation router."""
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
    # Filter out Webpack HMR logs to clean up console output
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
    return {"message": "Backend is running!"}


@app.get("/health")
def health():
    return {"status": "OK", "healthy": True}


app.include_router(api_router, tags=["Recommendation & Explore"])