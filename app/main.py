from fastapi import FastAPI
import http3
from fastapi.middleware.cors import CORSMiddleware
from .routers import login, signup, users, voyage_passenger
from .routers import voyage_driver, admin

app = FastAPI()
client = http3.AsyncClient()


async def call_api(url: str):
    r = await client.get(url)
    return r.text

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://taller-2-tyrions.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(signup.router)
app.include_router(users.router)
app.include_router(voyage_passenger.router)
app.include_router(voyage_driver.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    result = await call_api('https://fiuber-users.herokuapp.com/')
    return {"Msg from users": result}
