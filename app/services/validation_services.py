import requests
from fastapi.encoders import jsonable_encoder
import os
from fastapi.exceptions import HTTPException

USERS_URL = os.getenv("USERS_URL")


def is_status_correct(status_code):
    return status_code//100 == 2


def validate_request_and_get_uid(_token):
    resp0 = requests.post(USERS_URL+"/validate", json=jsonable_encoder(_token))
    print("resp0: "+str(resp0))
    if (is_status_correct(resp0.status_code)):
        resp = resp0.json()
        print("resp: "+resp)
        if (resp["is_blocked"] or "User" not in resp["roles"]):
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
