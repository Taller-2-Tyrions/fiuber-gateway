from fastapi import APIRouter
from firebase_admin import auth
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

router = APIRouter(
    prefix="/signup",
    tags=['Users']
)

@router.post('/')
async def signup(email: str, password: str):
   if email is None or password is None:
       return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
   try:
       user = auth.create_user(
           email=email,
           password=password
       )
       return JSONResponse(content={'message': f'Successfully created user {user.uid}'}, status_code=200)    
   except:
       return HTTPException(detail={'message': 'Error Creating User'}, status_code=400)
