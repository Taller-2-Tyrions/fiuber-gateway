from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ..schemas.users_schema import UserBase, DriverBase
from fastapi.encoders import jsonable_encoder
import requests
from fastapi import Cookie
from typing import Union, Optional
from dotenv import load_dotenv
import os

load_dotenv()
USERS_URL = os.getenv("USERS_URL")


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post('/')
async def create_user(user: Union[UserBase, DriverBase], token: Union[str, None] = Cookie(None)):
    params = {
        "token": token
    }
    req = requests.post(USERS_URL+"/validate", json=params)
    print(req.json())
    if (req.status_code == 200):
        user = jsonable_encoder(user)
        user.id = req.json()["uid"]
        req = requests.post(USERS_URL+"/users", json=user)
    else:
        raise HTTPException(detail=req.json()["detail"],
                            status_code=req.status_code)
