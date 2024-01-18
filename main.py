from fastapi import FastAPI
from app.api import endpoints
from app.db.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(endpoints.router, prefix="/v1")
