from fastapi import FastAPI
from app.api.endpoints import router
from app.db.database import database

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup_db_client():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
