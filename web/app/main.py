from fastapi import FastAPI
from api.routers import genera, users

app = FastAPI()

app.include_router(genera.router, prefix="/genera", tags=["Genera"])
app.include_router(users.router, prefix="/users", tags=["Users"])
@app.get("/")
async def read_root():
    return {"": "🦕 Welcome to the Mesozoic Era! 🦖"}

