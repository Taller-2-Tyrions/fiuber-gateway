from fastapi import FastAPI
import http3
from fastapi.middleware.cors import CORSMiddleware

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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    result = await call_api('https://fiuber-users.herokuapp.com/')
    return {"Msg from users": result}
