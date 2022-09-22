from fastapi import APIRouter
from ..schemas.users_schema import AuthBase
from fastapi.exceptions import HTTPException
import requests
from dotenv import load_dotenv
import os
from fastapi.encoders import jsonable_encoder

load_dotenv()
USERS_URL = os.getenv("USERS_URL")

router = APIRouter(
    prefix="/signup",
    tags=['Sign Up']
)


@router.post('/')
async def signup(params: AuthBase):
    req = requests.post(USERS_URL+"/signup", json=jsonable_encoder(params))

    data = req.json()
    if (req.status_code != 200):
        raise HTTPException(detail=data["detail"], status_code=req.status_code)
    return data
