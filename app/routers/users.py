from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ..schemas.users_schema import UserBase, DriverBase
from fastapi.encoders import jsonable_encoder
import requests
from fastapi import Cookie
from typing import Optional, Union
from dotenv import load_dotenv
import os

load_dotenv()
USERS_URL = os.getenv("USERS_URL")


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


def is_status_correct(status_code):
    return status_code//100 == 2


@router.post('/')
async def create_user(user: Union[UserBase, DriverBase],
                      token: Optional[str] = Cookie(None)):
    params = {
        "token": token
    }
    req = requests.post(USERS_URL+"/validate", json=params)
    if (is_status_correct(req.status_code)):
        user = jsonable_encoder(user)
        id = req.json()["uid"]
        user["id"] = id
        user["is_blocked"] = False
        profile_picture = user["profile_picture"]
        delattr(user, "profile_picture")
        req = requests.post(USERS_URL+"/users", json=user)
        if (not is_status_correct(req.status_code)):
            data = req.json()
            raise HTTPException(detail=data["detail"],
                                status_code=req.status_code)
        if profile_picture:
            img = {"img": profile_picture}
            req = requests.post(USERS_URL+"/"+id+"/profile/picture", json=img)

    else:
        raise HTTPException(detail=req.json()["detail"],
                            status_code=req.status_code)


@router.delete('/{id_user}')
async def delete_user(id_user: str, token: Optional[str] = Cookie(None)):
    params = {
        "token": token
    }
    req = requests.post(USERS_URL+"/validate", json=params)
    if (is_status_correct(req.status_code)):
        caller_id = req.json()["uid"]
        req = requests.delete(USERS_URL + "/users/" +
                              id_user + "?user_caller=" + caller_id)
        if (not is_status_correct(req.status_code)):
            data = req.json()
            raise HTTPException(detail=data["detail"],
                                status_code=req.status_code)
    else:
        raise HTTPException(detail=req.json()["detail"],
                            status_code=req.status_code)


@router.get('/{id_user}')
async def find_user(id_user: str, token: str):
    # TODO: ADD COOKIE -> token: Optional[str] = Cookie(None)):
    params = {
        "token": token
    }
    req = requests.post(USERS_URL+"/validate", json=params)
    if (is_status_correct(req.status_code)):
        caller_id = req.json()["uid"]
        req = requests.get(USERS_URL + "/users/" +
                           id_user + "?user_caller=" + caller_id)
        data = req.json()
        if (not is_status_correct(req.status_code)):
            raise HTTPException(detail=data["detail"],
                                status_code=req.status_code)
        req = requests.get(USERS_URL+"/"+id_user+"/profile/picture")
        if is_status_correct(req.status_code):
            data["profile_picture"] = req.json().get("img")
    else:
        raise HTTPException(detail=req.json()["detail"],
                            status_code=req.status_code)
