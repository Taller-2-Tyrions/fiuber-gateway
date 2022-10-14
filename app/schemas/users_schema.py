from pydantic import BaseModel
from typing import List
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


class ProfilePictureBase(BaseModel):
    img: str


class PersonBase(BaseModel):
    name: str
    last_name: str
    roles: List[Roles]


class UserBase(PersonBase):
    address: str


class DriverBase(PersonBase):
    car: CarBase


class AuthBase(BaseModel):
    email: str
    password: str


class RecoveryEmailBase(BaseModel):
    email: str
