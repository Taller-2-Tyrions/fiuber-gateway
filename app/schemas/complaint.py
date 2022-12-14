from pydantic import BaseModel
from enum import Enum
from typing import Optional


class ComplaintType(Enum):
    STEAL = "STEAL"
    SEXUAL_ASSAULT = "SEXUAL"
    UNSAFE_DRIVING = "UNSAFE DRIVING"
    UNSAFE_CAR = "UNSAFE CAR"
    UNDER_INFLUENCE = "UNDER INFLUENCE"
    AGGRESIVE = "AGGRESIVE"


class ReviewBase(BaseModel):
    score: int
    comment: Optional[str]


class ComplaintBase(BaseModel):
    complaint_type: ComplaintType
    description: str
