import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.recommendation import router as recommendation_router
from app.routers.explore import router as explore_router

app = FastAPI(
    title="DriveMatch AI API",
    version="1.0.0",
    description="Smart Car Recommendation System"
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
    return {"message": "Backend running successfully"}


@app.get("/health")
def health():
    return {"status": "OK"}


app.include_router(recommendation_router, tags=["Recommendation"])
app.include_router(explore_router, tags=["Explore"])