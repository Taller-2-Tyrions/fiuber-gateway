from typing import Optional
from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os
from app.schemas.complaint import ComplaintBase, ReviewBase
from app.schemas.voyage_schema import SearchVoyageBase
import requests
from fastapi.encoders import jsonable_encoder
from ..services.validation_services import validate_req_passenger_and_get_uid


load_dotenv()
VOYAGE_URL = os.getenv("VOYAGE_URL")


router = APIRouter(
    prefix="/voyage/passenger",
    tags=['Voyage']
)


def is_status_correct(status_code):
    return status_code//100 == 2


@router.post('/vip/subscription')
def passenger_subscribes_to_vip(token: Optional[str] = Header(None)):
    """
    A Passenger subscribes to VIP Package.
    """
    uid = validate_req_passenger_and_get_uid(token)
    resp = requests.post(VOYAGE_URL
                         + "/voyage/passenger/vip/"+uid+"/"+"/true")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/vip/unsubscription')
def passenger_unsubscribes_to_vip(token: Optional[str] = Header(None)):
    """
    A Passenger unsubscribes to VIP Package.
    """
    uid = validate_req_passenger_and_get_uid(token)
    resp = requests.post(VOYAGE_URL
                         + "/voyage/passenger/vip/"+uid+"/"+"/false")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/search')
async def start_searching(voyage: SearchVoyageBase,
                          token: Optional[str] = Header(None)):
    """
    Passenger Search For All Nearest Drivers
    """
    uid = validate_req_passenger_and_get_uid(token)

    voyage_body = jsonable_encoder(voyage)

    voyage_body["passenger_id"] = uid

    resp = requests.post(VOYAGE_URL+"/voyage/passenger/search",
                         json=voyage_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/search/{id_driver}')
async def ask_for_voyage(id_driver: str, voyage: SearchVoyageBase,
                         token: Optional[str] = Header(None)):
    """
    Passenger Chose a Driver.
    """
    uid = validate_req_passenger_and_get_uid(token)

    voyage_body = jsonable_encoder(voyage)

    voyage_body["passenger_id"] = uid

    resp = requests.post(VOYAGE_URL+"/voyage/passenger/search/"+id_driver,
                         json=voyage_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.delete('/search')
def cancel_search(token: Optional[str] = Header(None)):
    """
    Client Cancels Voyage Search
    """
    uid = validate_req_passenger_and_get_uid(token)
    resp = requests.delete(VOYAGE_URL
                           + "/voyage/passenger/search/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/complaint/{voyage_id}')
def add_passanger_complaint(voyage_id: str, complaint: ComplaintBase,
                            token: Optional[str] = Header(None)):
    """
    Passenger Load A Complaint Of Voyage
    """
    uid = validate_req_passenger_and_get_uid(token)
    resp = requests.post(VOYAGE_URL
                         + "/voyage/passenger/complaint/" +
                         voyage_id + "/" + uid,
                         json=jsonable_encoder(complaint))
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.delete('/{voyage_id}')
def cancel_confirmed_voyage(voyage_id: str,
                            token: Optional[str] = Header(None)):
    """
    Cancel Voyage Previously Confirmed By Passenger
    """
    uid = validate_req_passenger_and_get_uid(token)
    resp = requests.delete(VOYAGE_URL
                           + "/voyage/" + voyage_id + "/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.get('/last')
def get_lasts_voyages(token: Optional[str] = Header(None)):
    """
    Get last voyages made by passenger
    """
    uid = validate_req_passenger_and_get_uid(token)
    resp = requests.get(VOYAGE_URL
                        + "/voyage/last/" + uid + "/false")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/review/{voyage_id}')
def add_review(voyage_id: str, review: ReviewBase,
               token: Optional[str] = Header(None)):
    """
    Add a review from passenger to driver.
    """
    uid = validate_req_passenger_and_get_uid(token)
    rev = jsonable_encoder(review)
    rev["by_driver"] = False
    resp = requests.post(VOYAGE_URL
                         + "/voyage/review/" + voyage_id + "/" + uid,
                         json=rev)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data
