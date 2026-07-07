from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    budget: float = Field(..., gt=0)
    fuel_type: str
    transmission: str
    body_type: str
    seating: int = Field(..., ge=2)
    min_mileage: float = Field(..., ge=0)
    min_safety: float = Field(..., ge=0, le=5)