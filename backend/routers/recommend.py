"""FastAPI router defining the HTTP POST endpoint for car recommendation queries."""
from fastapi import APIRouter
from schemas.request import RecommendationRequest
from schemas.response import RecommendationResponse
from recommender.services import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()


@router.post("/recommend", response_model=RecommendationResponse)
def recommend_car(user_input: RecommendationRequest):
    """Generates a ranked list of car recommendations based on user preferences."""
    recommended_cars = recommendation_service.get_recommendations(user_input.model_dump())
    return {"recommendations": recommended_cars}
