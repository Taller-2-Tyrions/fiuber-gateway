from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os
from ..schemas.users_schema import TokenBase
from app.schemas.voyage_schema import SearchVoyageBase
import requests
from fastapi.encoders import jsonable_encoder
from ..services.validation_services import validate_request_and_get_uid


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
    uid = validate_request_and_get_uid(token)

    voyage_body = jsonable_encoder(voyage)
    
    voyage_body["passenger"]["id"] = uid

    resp = requests.post(VOYAGE_URL+"/voyage/user", json=voyage_body)
    data = resp.json()
    if (not is_status_correct(resp.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=resp.status_code)
    return data
