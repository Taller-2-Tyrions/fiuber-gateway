from typing import Optional
from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os
from app.schemas.complaint import ReviewBase
from app.schemas.voyage_schema import Point
import requests
from fastapi.encoders import jsonable_encoder
from ..services.validation_services import validate_req_driver_and_get_uid


load_dotenv()
VOYAGE_URL = os.getenv("VOYAGE_URL")
PAYMENTS_URL = os.getenv("PAYMENTS_URL")


router = APIRouter(
    prefix="/voyage/driver",
    tags=['Driver endpoints in Voyage']
)


def is_status_correct(status_code):
    return status_code//100 == 2


@router.post('/searching')
def activate_driver(location: Point,
                    token: Optional[str] = Header(None)):
    """
    Add Driver To Is Searching List
    """
    uid = validate_req_driver_and_get_uid(token)
    location_body = jsonable_encoder(location)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/searching/"+uid,
                         json=location_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/offline')
def deactivate_driver(token: Optional[str] = Header(None)):
    """
    A Seaching driver is set to Offline.
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/offline/"+uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/vip/subscription')
def driver_subscribes_to_vip(token: Optional[str] = Header(None)):
    """
    A Driver subscribes to VIP Package.
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/vip/"+uid+"/true")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/vip/unsubscription')
def driver_unsubscribes_vip(token: Optional[str] = Header(None)):
    """
    A Driver leaves VIP Package.
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/vip/"+uid+"/false")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/location')
def update_location(location: Point, token: Optional[str] = Header(None)):
    """
    Updates the Driver location in real time.
    """
    location_body = jsonable_encoder(location)
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/location/"+uid,
                         json=location_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/reply/{id_voyage}/{status}')
def reply_voyage_solicitation(id_voyage: str, status: bool,
                              token: Optional[str] = Header(None)):
    """
    Driver Acepts (True) / Declines (False) passenger solicitation
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/reply/"
                         + id_voyage + "/" + str(status) + "/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/start/{voyage_id}')
def inform_start_voyage(voyage_id: str,
                        token: Optional[str] = Header(None)):
    """
    Driver Informs Arrived at Initial Point.
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/start/" +
                         voyage_id + "/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/end/{voyage_id}')
def inform_finish_voyage(voyage_id: str,
                         token: Optional[str] = Header(None)):
    """
    Driver Informs Voyage Has Finished.
    """
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.post(VOYAGE_URL+"/voyage/driver/end/"
                         + voyage_id + "/" + uid)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    resp = requests.get(VOYAGE_URL
                        + "/voyage/" + voyage_id)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)

    params = {"senderId": data["passenger_id"],
              "receiverId": data["driver_id"],
              "amountInEthers": 0.0000001}
    # En AMOUNT VA data['price'] pero hay que ver si manejamos ethers
    #  o pesos/dolares
    # Ya que payments espera en eths pero en voyage lo tenemos en pesos/dolares
    # Tambien le vamos a pasar el fee que nos quedamos nosotros de ese monto

    resp = requests.post(PAYMENTS_URL+"/deposit",
                         json=params)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return {"result": "Ok"}


@router.delete('/voyage/{voyage_id}')
def cancel_confirmed_voyage(voyage_id: str,
                            token: Optional[str] = Header(None)):
    """
    Cancel Voyage Previously Confirmed By Passenger
    """
    uid = validate_req_driver_and_get_uid(token)
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
    uid = validate_req_driver_and_get_uid(token)
    resp = requests.get(VOYAGE_URL
                        + "/voyage/last/" + uid + "/true")
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data


@router.post('/review/{voyage_id}')
def add_review(voyage_id: str, review: ReviewBase,
               token: Optional[str] = Header(None)):
    """
    Add a review from driver to passenger.
    """
    uid = validate_req_driver_and_get_uid(token)
    rev = jsonable_encoder(review)
    rev["by_driver"] = True
    resp = requests.post(VOYAGE_URL
                         + "/voyage/review/" + voyage_id + "/" + uid,
                         json=rev)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data
