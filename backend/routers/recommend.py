"""
API router module for recommendation endpoints.
Defines endpoints that handle user query parameters and return matching car results.
"""
from fastapi import APIRouter
from schemas.request import RecommendationRequest
from schemas.response import RecommendationResponse
from recommender.services import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_car(user_input: RecommendationRequest):
    
    recommended_cars = recommendation_service.recommend_cars(user_input.model_dump())
    return {"recommendations": recommended_cars}
