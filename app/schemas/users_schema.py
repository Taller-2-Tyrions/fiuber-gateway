from pydantic import BaseModel
from typing import List
from enum import Enum


class Roles(Enum):
    PASSENGER = "Passenger"
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


class PassengerBase(PersonBase):
    address: str


class DriverBase(PersonBase):
    car: CarBase


class AuthBase(BaseModel):
    email: str
    password: str


class LoginAuthBase(AuthBase):
    device_token: str


class RecoveryEmailBase(BaseModel):
    email: str


class DeviceToken(BaseModel):
    device_token: str
