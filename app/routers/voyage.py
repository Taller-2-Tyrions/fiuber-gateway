from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
import os
from ..schemas.users_schema import TokenBase
from app.schemas.voyage_schema import SearchVoyageBase
import requests
from fastapi.encoders import jsonable_encoder


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
    req = requests.post(USERS_URL+"/validate", json=jsonable_encoder(token))
    if (is_status_correct(req.status_code)):
        resp = req.json()
        if (resp["is_blocked"] or "User" not in resp["roles"]):
            raise HTTPException(detail={
                'message': 'Error Permission Denied',
                'is_blocked': resp["is_blocked"],
                'roles': resp["roles"]
            }, status_code=400)

        voyage = jsonable_encoder(voyage)
        id = req.json()["uid"]
        voyage["id"] = id
        req = requests.post(VOYAGE_URL+"/voyage/user", json=voyage)
        if (not is_status_correct(req.status_code)):
            data = req.json()
            raise HTTPException(detail=data["detail"],
                                status_code=req.status_code)
        return req.json()
    else:
        raise HTTPException(detail=req.json()["detail"],
                            status_code=req.status_code)
