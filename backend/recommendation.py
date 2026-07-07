from fastapi import APIRouter

from schemas.request import RecommendationRequest
from schemas.response import RecommendationResponse
from services import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()

@router.post("/recommend", response_model=RecommendationResponse)
def recommend_car(user_input: RecommendationRequest):
    # get the best car matches based on user form input
    recommended_cars = recommendation_service.recommend_cars(user_input.model_dump())
    
    return {"recommendations": recommended_cars}


