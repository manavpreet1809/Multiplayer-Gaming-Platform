from fastapi import FastAPI

from api.auth import router as auth_router
from db.validUser_mongo import create_indexes, close_mongo_connection

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_indexes()


@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()


app.include_router(auth_router)