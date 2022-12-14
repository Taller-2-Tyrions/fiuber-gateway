from pydantic import BaseModel


class ConstantsBase(BaseModel):
    price_meter: float
    price_minute: float
    price_vip: float
    plus_night: float
    seniority_driver: float
    daily_driver: float
    monthly_driver: float
    seniority_passenger: float
    daily_passenger: float
    monthly_passenger: float
    max_discount_passenger: float
    max_increase_driver: float
