from fastapi import APIRouter, Header
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from app.services.validation_services import validate_req_admin_and_get_uid
from typing import Optional
import requests
import os
from ..schemas.pricing import ConstantsBase

load_dotenv()
USERS_URL = os.getenv("USERS_URL")
PRICING_URL = os.getenv("PRICING_URL")
VOYAGE_URL = os.getenv("VOYAGE_URL")


router = APIRouter(
    prefix="/admin",
    tags=['Admin Routes']
)


def is_status_correct(status_code):
    return status_code//100 == 2


@router.post('/register/{user_id}')
async def register_admin(user_id: str,
                         token: Optional[str] = Header(None)):
    """
    Add Admin rol to user
    """
    caller_id = validate_req_admin_and_get_uid(token)
    req = requests.post(USERS_URL+f"/users/admin/{user_id}/{caller_id}")
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    return data


@router.post('/block/{user_id}')
async def block_user(user_id: str,
                     token: Optional[str] = Header(None)):
    """
    Block User
    """
    caller_id = validate_req_admin_and_get_uid(token)
    req = requests.post(USERS_URL+f"/users/block/{user_id}/{caller_id}")
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    return data


@router.post('/unblock/{user_id}')
async def unblock_user(user_id: str,
                       token: Optional[str] = Header(None)):
    """
    Unblock User
    """
    caller_id = validate_req_admin_and_get_uid(token)
    req = requests.post(USERS_URL+f"/users/unblock/{user_id}/{caller_id}")
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    return data


@router.get('/users')
async def get_users(token: Optional[str] = Header(None)):
    """
    Get Info From All The Users In Database
    """
    caller_id = validate_req_admin_and_get_uid(token)
    req = requests.get(USERS_URL+f"/users/all/{caller_id}")
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    return data


@router.get('/complaints')
async def get_complaints(token: Optional[str] = Header(None)):
    """
    Get Info From All The Complaints In Database
    """
    validate_req_admin_and_get_uid(token)
    req = requests.get(VOYAGE_URL+"/voyage/complaints")
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    return data


@router.get('/constants')
async def get_constants(token: Optional[str] = Header(None)):
    """
    Get Pricing Constants
    """
    validate_req_admin_and_get_uid(token)
    req = requests.get(f"{PRICING_URL}/admin")
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    return data


@router.put('/constants')
async def put_constants(new_constants: ConstantsBase,
                        token: Optional[str] = Header(None)):
    """
    Get Pricing Constants
    """
    validate_req_admin_and_get_uid(token)
    req = requests.put(f"{PRICING_URL}/admin",
                       json=jsonable_encoder(new_constants))
    data = req.json()
    if (not is_status_correct(req.status_code)):
        raise HTTPException(detail=data["detail"],
                            status_code=req.status_code)
    return data
