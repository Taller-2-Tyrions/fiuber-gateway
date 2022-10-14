import requests
import os
from fastapi.exceptions import HTTPException

USERS_URL = os.getenv("USERS_URL")


def is_status_correct(status_code):
    return status_code//100 == 2


def validate_token(token):
    params = {
        "token": token
    }
    resp = requests.post(USERS_URL+"/validate", json=params)
    if (is_status_correct(resp.status_code)):
        return resp.json()["uid"]
    raise HTTPException(detail={
                'message': resp.reason
            }, status_code=resp.status_code)


def validate_req_and_get_uid(token, role):
    params = {
        "token": token
    }
    resp0 = requests.post(USERS_URL+"/validate", json=params)
    if (is_status_correct(resp0.status_code)):
        resp = resp0.json()
        if (resp["is_blocked"] or role not in resp["roles"]):
            raise HTTPException(detail={
                'message': 'Error Permission Denied',
                'is_blocked': resp["is_blocked"],
                'roles': resp["roles"]
            }, status_code=400)
    else:
        raise HTTPException(detail={
                'message': resp0.reason
            }, status_code=resp0.status_code)
    return resp["uid"]


def validate_req_driver_and_get_uid(token):
    validate_req_and_get_uid(token, "Driver")


def validate_req_user_and_get_uid(token):
    validate_req_and_get_uid(token, "User")
