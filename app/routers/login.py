from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from ..firebase_configs import get_pb

router = APIRouter(
    prefix="/login",
    tags=['Users']
)

@router.post('/')
async def login(email: str, password: str):
   try:
       user = get_pb().auth().sign_in_with_email_and_password(email, password)
       jwt = user['idToken']
       return JSONResponse(content={'token': jwt}, status_code=200)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400)
