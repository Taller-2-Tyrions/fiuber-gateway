from pydantic import BaseModel
from typing import List


class CarBase(BaseModel):
    model: str
    year: int
    plaque: str
    capacity: int


class PersonBase(BaseModel):
    name: str
    last_name: str
    roles: List[str]


class UserBase(PersonBase):
    address: str


class DriverBase(PersonBase):
    car: CarBase


class AuthBase(BaseModel):
    email: str
    password: str


class TokenBase(BaseModel):
    token: str
