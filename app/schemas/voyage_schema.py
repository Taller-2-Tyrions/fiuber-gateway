from pydantic import BaseModel


class Point(BaseModel):
    longitude: float
    latitude: float


class SearchVoyageBase(BaseModel):
    init: Point
    end: Point
    is_vip: bool
