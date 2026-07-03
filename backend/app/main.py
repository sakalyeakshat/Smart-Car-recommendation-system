
from fastapi import FastAPI
from app.routers.recommendation import router as recommendation_router

app = FastAPI()

app.include_router(recommendation_router)

@app.get("/")
def home():
    return {"message": "Backend running"}