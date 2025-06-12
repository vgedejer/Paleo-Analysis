from fastapi import FastAPI
from api.routers import genera

app = FastAPI()

app.include_router(genera.router)
@app.get("/")
async def read_root():
    return {"": "🦕 Welcome to the Mesozoic Era! 🦖"}

