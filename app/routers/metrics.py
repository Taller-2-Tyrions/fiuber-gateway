from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from app.services.validation_services import validate_req_admin_and_get_uid
from app.services.validation_services import validate_token
from app.services.validation_services import validate_req_driver_and_get_uid
from ..schemas.users_schema import Roles, PassengerBase, DriverBase
from ..schemas.users_schema import ProfilePictureBase
from ..schemas.users_schema import WithdrawBase
from fastapi.encoders import jsonable_encoder
import requests
from typing import Optional, Union
from dotenv import load_dotenv
import os

load_dotenv()
USERS_URL = os.getenv("USERS_URL")
METRICS_URL = os.getenv("METRICS_URL")


router = APIRouter(
    prefix="/metrics",
    tags=['Metrics']
)


def is_status_correct(status_code):
    return status_code//100 == 2


@router.get('/voyages')
async def get_voyages_metrics(token: Optional[str] = Header(None)):
    validate_req_admin_and_get_uid(token)
    resp = requests.get(METRICS_URL+"/metrics/voyages")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.get('/payments')
async def get_payments_metrics(token: Optional[str] = Header(None)):
    validate_req_admin_and_get_uid(token)
    resp = requests.get(METRICS_URL+"/metrics/payments")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.get('/users')
async def get_users_metrics(token: Optional[str] = Header(None)):
    validate_req_admin_and_get_uid(token)
    resp = requests.get(METRICS_URL+"/metrics/users")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data
