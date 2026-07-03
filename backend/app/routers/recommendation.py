from fastapi import APIRouter

from app.schemas.request import RecommendationRequest
from app.schemas.response import RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()

recommendation_service = RecommendationService()


@router.post(
    "/recommend",
    response_model=RecommendationResponse
)
def recommend_car(user_input: RecommendationRequest):

    recommended_cars = recommendation_service.recommend_cars(
        user_input.model_dump()
    )

    return {
        "recommendations": recommended_cars
    }