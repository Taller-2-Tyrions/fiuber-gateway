from typing import Optional
from fastapi import APIRouter, status, Header
from fastapi.exceptions import HTTPException
from ..schemas.users_schema import LoginAuthBase, RecoveryEmailBase
from ..schemas.users_schema import DeviceToken
from fastapi.encoders import jsonable_encoder
import requests
from dotenv import load_dotenv
import os
from app.services.rabbit_services import push_metric

load_dotenv()
USERS_URL = os.getenv("USERS_URL")

router = APIRouter(
    prefix="/login",
    tags=['Login']
)


@router.post('/password-recovery', status_code=status.HTTP_200_OK)
async def send_recover_email(email: RecoveryEmailBase):
    req = requests.post(USERS_URL+"/login/password-recovery",
                        json=jsonable_encoder(email))
    data = req.json()
    if (req.status_code != status.HTTP_200_OK):
        raise HTTPException(detail=data["detail"], status_code=req.status_code)


@router.post('/')
async def login(params: LoginAuthBase):
    req = requests.post(USERS_URL+"/login", json=jsonable_encoder(params))

    data = req.json()

    status = req.status_code == 200
    push_metric({"event": "Login",
                "is_federated": False,
                 "status": status})

    if (req.status_code != 200):
        raise HTTPException(detail=data["detail"], status_code=req.status_code)
    return data


@router.post('/google')
async def login_google(device_token: DeviceToken,
                       token: Optional[str] = Header(None)):
    params = jsonable_encoder(device_token)
    params["token"] = token
    req = requests.post(USERS_URL+"/login/google",
                        json=params)

    data = req.json()

    status = req.status_code == 200
    push_metric({"event": "Login",
                "is_federated": True,
                 "status": status})

    if (req.status_code != 200):
        raise HTTPException(detail=data["detail"], status_code=401)
    return data
