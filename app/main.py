from fastapi import FastAPI
from pydantic import BaseModel

from app.database.database import Base, engine
from app.database import models
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/api")


class HomeResponse(BaseModel):
    message: str


@app.get("/", response_model=HomeResponse)
def home():
    return {
        "message": "Geospatial File Measurement API is running"
    }