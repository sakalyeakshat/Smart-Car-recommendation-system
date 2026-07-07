"""
Recommendation router module.
Exposes the API endpoints related to generating car recommendations.
"""
from fastapi import APIRouter

from schemas.request import RecommendationRequest
from schemas.response import RecommendationResponse
from services import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()

@router.post("/recommend", response_model=RecommendationResponse)
def recommend_car(user_input: RecommendationRequest):
    """
    Evaluates user preferences and returns the top recommended cars.
    """
    recommended_cars = recommendation_service.recommend_cars(user_input.model_dump())
    
    return {"recommendations": recommended_cars}


