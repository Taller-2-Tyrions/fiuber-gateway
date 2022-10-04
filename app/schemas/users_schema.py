from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Roles(Enum):
    USER = "User"
    DRIVER = "Driver"
    ADMIN = "Admin"


class CarBase(BaseModel):
    model: str
    year: int
    plaque: str
    capacity: int


class PersonBase(BaseModel):
    name: str
    last_name: str
    roles: List[Roles]
    profile_picture: Optional[str] = None


class UserBase(PersonBase):
    address: str


class DriverBase(PersonBase):
    car: CarBase


class AuthBase(BaseModel):
    email: str
    password: str


class TokenBase(BaseModel):
    token: str


class RecoveryEmailBase(BaseModel):
    email: str
