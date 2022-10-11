from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os
from ..schemas.users_schema import TokenBase
from app.schemas.voyage_schema import DriverBaseVoyage, SearchVoyageBase
import requests
from fastapi.encoders import jsonable_encoder
from ..services.validation_services import validate_req_user_and_get_uid
from ..services.validation_services import validate_req_driver_and_get_uid


load_dotenv()
USERS_URL = os.getenv("USERS_URL")
VOYAGE_URL = os.getenv("VOYAGE_URL")


router = APIRouter(
    prefix="/voyage",
    tags=['Voyage']
)


def is_status_correct(status_code):
    return status_code//100 == 2


@router.post('/user')
async def init_voyage(voyage: SearchVoyageBase, token: TokenBase):
    """
    Client Search For All Nearest Drivers
    """
    uid = validate_req_user_and_get_uid(token)

    voyage_body = jsonable_encoder(voyage)

    voyage_body["passenger"]["id"] = uid

    resp = requests.post(VOYAGE_URL+"/voyage/user", json=voyage_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/user/{id_driver}')
async def ask_for_voyage(id_driver: str, voyage: SearchVoyageBase,
                         token: TokenBase):
    """
    Client Chose a Driver.
    """
    uid = validate_req_user_and_get_uid(token)

    voyage_body = jsonable_encoder(voyage)

    voyage_body["passenger"]["id"] = uid

    resp = requests.post(VOYAGE_URL+"/voyage/user/"+id_driver,
                         json=voyage_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.delete('/user/voyage_search')
def cancel_search(token: TokenBase):
    """
    Client Cancels Voyage Search
    """
    uid = validate_req_user_and_get_uid(token)
    resp = requests.delete(VOYAGE_URL
                           + "/voyage/voyage_search/?passenger_id=" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.delete('/user/voyage/{voyage_id}')
def cancel_confirmed_voyage(voyage_id: str, token: TokenBase):
    """
    Cancel Voyage Previously Confirmed By Client
    """
    uid = validate_req_user_and_get_uid(token)
    resp = requests.delete(VOYAGE_URL
                           + "/voyage/voyage/" + voyage_id + "/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/driver')
def add_driver(driver: DriverBaseVoyage, token: TokenBase):
    """
    Add Driver To Searching List
    """
    uid = validate_req_driver_and_get_uid(token)

    driver_body = jsonable_encoder(driver)

    driver_body["id"] = uid

    resp = requests.post(VOYAGE_URL+"/voyage/driver/", json=driver_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/driver/{id_voyage}/{status}')
def accept_voyage(id_voyage: str, status: bool, token: TokenBase):
    """
    Driver Acepts (True) / Declines (False) client solicitation
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/"
                         + id_voyage + "/" + str(status) + "?driver_id=" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/driver/start/{voyage_id}')
def inform_start_voyage(voyage_id: str, token: TokenBase):
    """
    Inform Driver Arrived Initial Point
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/start/" + voyage_id + "/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/driver/finish/{voyage_id}')
def inform_finish_voyage(voyage_id: str, token: TokenBase):
    """
    Inform Voyage Has Finished
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/finish/" + voyage_id + "/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data
