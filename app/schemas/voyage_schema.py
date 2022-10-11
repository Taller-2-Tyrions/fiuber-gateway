from pydantic import BaseModel
from enum import Enum


class Point(BaseModel):
    longitude: float
    latitude: float


class DriverStatus(Enum):
    SEARCHING = "SEARCHING"  # esta totalmente libre
    WAITING = "WAITING"  # Viaje Confirmado Cliente
    GOING = "GOING"  # Viaje Confirmado Ambos
    TRAVELLING = "TRAVELLING"  # Ya con Cliente
    OFFLINE = "OFFLINE"  # No espero viajes


class PassengerStatus(Enum):
    CHOOSING = "CHOOSING"  # Decidiendo Choferes / estado pasivo.
    WAITING_CONFIRMATION = "WAITING_CONFIRMATION"  # Viaje Confirmado Cliente
    WAITING_DRIVER = "WAITING_DRIVER"  # Viaje Confirmado Ambos
    TRAVELLING = "TRAVELLING"  # Ya con Cliente


class VoyageStatus(Enum):
    WAITING = "WAITING"  # Viaje Confirmado Cliente
    STARTING = "STARTING"  # Chofer Yendo A Cliente
    TRAVELLING = "TRAVELLING"  # Ya con Cliente
    FINISHED = "FINISHED"  # Viaje Confirmado Ambos


class DriverBase(BaseModel):
    status: DriverStatus
    location: Point


class PassengerBase(BaseModel):
    status: PassengerStatus
    location: Point


class SearchVoyageBase(BaseModel):
    passenger: PassengerBase
    init: Point
    end: Point


class VoyageBase(BaseModel):
    passenger_id: str
    driver_id: str
    init: Point
    end: Point
    status: VoyageStatus
    price: float
