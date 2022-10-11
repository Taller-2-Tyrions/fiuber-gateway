import requests
from fastapi.encoders import jsonable_encoder
import os
from fastapi.exceptions import HTTPException

USERS_URL = os.getenv("USERS_URL")


def is_status_correct(status_code):
    return status_code//100 == 2


def validate_request_and_get_uid(_token):
    req = requests.post(USERS_URL+"/validate", json=jsonable_encoder(_token))
    if (is_status_correct(req.status_code)):
        resp = req.json()
        if (resp["is_blocked"] or "User" not in resp["roles"]):
            raise HTTPException(detail={
                'message': 'Error Permission Denied',
                'is_blocked': resp["is_blocked"],
                'roles': resp["roles"]
            }, status_code=400)
    return req.json()["uid"]
