"""Pydantic schemas for recommendation request validation."""
from typing import List, Optional
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    budget: float = Field(..., gt=0)
    fuel_type: List[str]
    transmission: List[str]
    body_type: str
    seating: int = Field(..., ge=2)
    min_mileage: float = Field(..., ge=0, le=30)
    min_safety: float = Field(..., ge=0, le=5)
    min_range: Optional[float] = Field(None, ge=0)