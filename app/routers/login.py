from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ..schemas.users_schema import AuthBase
from fastapi import Cookie
from typing import Union
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


@router.post('/')
async def login(params: AuthBase):
    req = requests.post(USERS_URL+"/login", json=jsonable_encoder(params))

    data = req.json()
    if (req.status_code != 200):
        raise HTTPException(detail=data["detail"], status_code=req.status_code)
    return data


@router.post('/google')
async def login_google(token: Union[str, None] = Cookie(None)):
    params = {
        "token": token
    }
    req = requests.post(USERS_URL+"/login/google",
                        json=jsonable_encoder(params))

    data = req.json()
    if (req.status_code != 200):
        raise HTTPException(detail=data["detail"], status_code=req.status_code)
    return data
