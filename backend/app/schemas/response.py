from typing import List

from pydantic import BaseModel


class CarRecommendation(BaseModel):
    brand: str
    model: str
    body_type: str
    price_range_lakh: str
    fuel_type: str
    transmission: str
    safety_rating: float
    match_percent: float
    match_reasons: List[str]


class RecommendationResponse(BaseModel):
    recommendations: List[CarRecommendation]