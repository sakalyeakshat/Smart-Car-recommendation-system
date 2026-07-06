from typing import List
from pydantic import BaseModel


class ExploreRequest(BaseModel):
    """
    Input payload for the /explore endpoint.

    Carries the three car attributes that drive the
    key-strengths and things-to-consider logic.
    """
    fuel_type: str
    transmission: str
    body_type: str


class ExploreResponse(BaseModel):
    """
    Response payload returned by the /explore endpoint.

    Attributes:
        key_strengths      : Positive highlights about the car.
        things_to_consider : Potential drawbacks or trade-offs.
    """
    key_strengths: List[str]
    things_to_consider: List[str]
