from fastapi import FastAPI
import http3

app = FastAPI()
client = http3.AsyncClient()


async def call_api(url: str):
    r = await client.get(url)
    return r.text


@app.get("/")
async def root():
    result = await call_api('https://fiuber-users.herokuapp.com/')
    return {"Msg from users": result}
