import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommendation import router as api_router

app = FastAPI(
    title="DriveMatch AI API",
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
    return {"message": "Backend is running!"}


@app.get("/health")
def health():
    return {"status": "OK", "healthy": True}


app.include_router(api_router, tags=["Recommendation & Explore"])