from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException

from app.services.validation_services import validate_req_passenger_and_get_uid
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
VOYAGE_URL = os.getenv("VOYAGE_URL")
PAYMENTS_URL = os.getenv("PAYMENTS_URL")


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
    if (Roles.PASSENGER.value in user.get("roles")):
        resp = requests.post(VOYAGE_URL+"/voyage/passenger/signup/"+id)
        data = resp.json()
        if (not is_status_correct(resp.status_code)):
            raise HTTPException(detail=data["detail"],
                                status_code=resp.status_code)
        req = requests.post(PAYMENTS_URL+"/wallet", json={"user_id": id})
        data = req.json()
        if (not is_status_correct(req.status_code)):
            raise HTTPException(detail=data["detail"],
                                status_code=req.status_code)
    elif (Roles.DRIVER.value in user.get("roles")):
        resp = requests.post(VOYAGE_URL+"/voyage/driver/signup/"+id)
        data = resp.json()
        if (not is_status_correct(resp.status_code)):
            raise HTTPException(detail=data["detail"],
                                status_code=resp.status_code)


@router.post('/profile/picture')
async def post_picture(user: ProfilePictureBase,
                       token: Optional[str] = Header(None)):
    id = validate_token(token)
    resp = requests.post(USERS_URL+"/users/"+id+"/profile/picture",
                         json=jsonable_encoder(user))
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)


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


def get_user_info(caller_id, id_user):
    req = requests.get(USERS_URL + "/users/" +
                       id_user + "/" + caller_id)
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    req = requests.get(USERS_URL+"/users/"+id_user+"/profile/picture")
    if is_status_correct(req.status_code):
        data["profile_picture"] = req.json().get("img")
    return data


@router.get('/{id_user}')
async def find_user(id_user: str, token: Optional[str] = Header(None)):
    caller_id = validate_token(token)
    return get_user_info(caller_id, id_user)


def request_modifications(id_user, user, caller_id):
    _user = jsonable_encoder(user)
    _user["is_blocked"] = False
    _user["id"] = id_user

    req = requests.put(USERS_URL + "/users/" + id_user
                       + "/" + caller_id,
                       json=_user)
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
    caller_id = validate_token(token)
    request_modifications(id_user, user, caller_id)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/signup/"+id_user)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)


def get_public_profile(id: str, token: str, is_driver: bool):
    caller_id = validate_token(token)
    data = get_user_info(caller_id, id)
    resp = requests.get(VOYAGE_URL +
                        "/voyage/calification/"+id+"/"+str(is_driver))
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=resp.json()["detail"],
                            status_code=resp.status_code)
    data.update(resp.json())

    resp = requests.get(VOYAGE_URL +
                        "/voyage/count/"+id+"/"+str(is_driver))
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=resp.json()["detail"],
                            status_code=resp.status_code)
    data.update(resp.json())

    resp = requests.get(VOYAGE_URL +
                        "/voyage/review/"+id+"/"+str(is_driver))
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=resp.json()["detail"],
                            status_code=resp.status_code)
    data.update(resp.json())

    return data


@router.get('/driver/balance')
async def get_driver_balance(token: Optional[str] = Header(None)):
    """
    Ask for driver balance
    """
    driver_id = validate_token(token)
    resp = requests.get(PAYMENTS_URL+"/payments/"+driver_id)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)

    res = {"balance": data['amount']}
    return res


@router.post('/withdraw')
async def withdraw(withdraw: WithdrawBase,
                   token: Optional[str] = Header(None)):
    """
    Withdraw money for driver
    """
    driver_id = validate_token(token)

    resp = requests.post(PAYMENTS_URL+'/withdraw',
                         json={"userId": driver_id,
                               "receiverAddress": withdraw.receiver_address,
                               "amountInEthers": withdraw.amount_in_ethers
                               })
    data = resp.json()

    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return {"hash": data['hash']}


@router.get('/passenger/balance')
async def get_passenger_balance(token: Optional[str] = Header(None)):
    """
    Ask for passenger balance
    """
    passenger_id = validate_token(token)
    resp = requests.get(PAYMENTS_URL+"/balance/"+passenger_id)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)

    res = {"balance": data['balance']}
    return res


@router.get('/driver/{id_driver}')
async def get_driver_profile(id_driver: str,
                             token: Optional[str] = Header(None)):
    """
    Ask for drivers public information
    """
    return get_public_profile(id_driver, token, True)


@router.get('/passenger/{id_passenger}')
async def get_passenger_profile(id_passenger: str,
                                token: Optional[str] = Header(None)):
    """
    Ask for passengers public information
    """
    return get_public_profile(id_passenger, token, False)


@router.post('/passenger/{id_user}')
async def add_passenger_role(id_user: str, user: DriverBase,
                             token: Optional[str] = Header(None)):
    """
    Add a passenger role to an user
    """
    caller_id = validate_token(token)
    request_modifications(id_user, user, caller_id)
    resp = requests.post(VOYAGE_URL+"/voyage/passenger/signup/"+id_user)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    req = requests.post(PAYMENTS_URL+"/wallet", json={"user_id": id_user})
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
