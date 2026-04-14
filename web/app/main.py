from fastapi import FastAPI
from api.routers import genera, users, fossils, species

app = FastAPI()

app.include_router(fossils.router, prefix="/fossils", tags=["Fossils"])
app.include_router(genera.router, prefix="/genera", tags=["Genera"])
app.include_router(species.router, prefix="/species", tags=["Species"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")

async def read_root():
    return {"": "🦕 Welcome to the Mesozoic Era! 🦖"}

