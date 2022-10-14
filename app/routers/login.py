from typing import Optional
from fastapi import APIRouter, status, Cookie
from fastapi.exceptions import HTTPException
from ..schemas.users_schema import AuthBase, RecoveryEmailBase
from fastapi.encoders import jsonable_encoder
import requests
from dotenv import load_dotenv
import os

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
async def login(params: AuthBase):
    req = requests.post(USERS_URL+"/login", json=jsonable_encoder(params))

    data = req.json()
    if (req.status_code != 200):
        raise HTTPException(detail=data["detail"], status_code=req.status_code)
    return data


@router.post('/google')
async def login_google(token: Optional[str] = Cookie(None)):
    params = {
        "token": token
    }
    req = requests.post(USERS_URL+"/login/google",
                        json=params)

    data = req.json()
    if (req.status_code != 200):
        raise HTTPException(detail=data["detail"], status_code=req.status_code)
    return data
