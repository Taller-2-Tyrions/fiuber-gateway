from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from app.services.validation_services import validate_req_passenger_and_get_uid
from app.services.validation_services import validate_token
from app.services.validation_services import validate_req_driver_and_get_uid
from ..schemas.users_schema import Roles, PassengerBase, DriverBase
from ..schemas.users_schema import ProfilePictureBase
from fastapi.encoders import jsonable_encoder
import requests
from typing import Optional, Union
from dotenv import load_dotenv
import os

load_dotenv()
USERS_URL = os.getenv("USERS_URL")
VOYAGE_URL = os.getenv("VOYAGE_URL")


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


def is_status_correct(status_code):
    return status_code//100 == 2


@router.post('/')
async def create_user(user: Union[PassengerBase, DriverBase],
                      token: Optional[str] = Header(None)):
    id = validate_token(token)
    user = jsonable_encoder(user)
    user["id"] = id
    user["is_blocked"] = False
    req = requests.post(USERS_URL+"/users", json=user)
    if (not is_status_correct(req.status_code)):
        data = req.json()
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    if (Roles.PASSENGER.value in user.roles):
        resp = requests.post(VOYAGE_URL+"/voyage/passenger/signup"+id)
        data = resp.json()
        if (not is_status_correct(resp.status_code)):
            raise HTTPException(detail=data["detail"],
                                status_code=resp.status_code)
    elif (Roles.DRIVER.value in user.roles):
        resp = requests.post(VOYAGE_URL+"/voyage/driver/signup"+id)
        data = resp.json()
        if (not is_status_correct(resp.status_code)):
            raise HTTPException(detail=data["detail"],
                                status_code=resp.status_code)


@router.post('/profile/picture')
async def post_picture(user: ProfilePictureBase,
                       token: Optional[str] = Header(None)):
    id = validate_token(token)
    return requests.post(USERS_URL+"/"+id+"/profile/picture",
                         json=jsonable_encoder(user))


@router.delete('/{id_user}')
async def delete_user(id_user: str,
                      token: Optional[str] = Header(None)):
    caller_id = validate_token(token)
    req = requests.delete(USERS_URL + "/users/" +
                          id_user + "/" + caller_id)
    if (not is_status_correct(req.status_code)):
        data = req.json()
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)


@router.get('/{id_user}')
async def find_user(id_user: str, token: Optional[str] = Header(None)):
    caller_id = validate_token(token)
    req = requests.get(USERS_URL + "/users/" +
                       id_user + "/" + caller_id)
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    req = requests.get(USERS_URL+"/"+id_user+"/profile/picture")
    if is_status_correct(req.status_code):
        data["profile_picture"] = req.json().get("img")
    return data


def request_modifications(id_user, user, caller_id):
    req = requests.put(USERS_URL + "/users/" + id_user
                       + "/" + caller_id,
                       json=jsonable_encoder(user))
    if (not is_status_correct(req.status_code)):
        data = req.json()
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)


@router.put('/passenger/{id_user}')
async def modify_passenger(id_user: str, user: PassengerBase,
                           token: Optional[str] = Header(None)):
    """
    Modify a Passenger
    """
    caller_id = validate_req_passenger_and_get_uid(token)
    request_modifications(id_user, user, caller_id)


@router.put('/driver/{id_user}')
async def modify_driver(id_user: str, user: DriverBase,
                        token: Optional[str] = Header(None)):
    """
    Modify a Driver
    """
    caller_id = validate_req_driver_and_get_uid(token)
    request_modifications(id_user, user, caller_id)


@router.post('/driver/{id_user}')
async def add_driver_role(id_user: str, user: DriverBase,
                          token: Optional[str] = Header(None)):
    """
    Add a driver role to an user
    """
    caller_id = validate_req_driver_and_get_uid(token)
    request_modifications(id_user, user, caller_id)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/signup"+id)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)


@router.post('/passenger/{id_user}')
async def add_passenger_role(id_user: str, user: DriverBase,
                             token: Optional[str] = Header(None)):
    """
    Add a passenger role to an user
    """
    caller_id = validate_req_passenger_and_get_uid(token)
    request_modifications(id_user, user, caller_id)
    resp = requests.post(VOYAGE_URL+"/voyage/passenger/signup"+id)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
