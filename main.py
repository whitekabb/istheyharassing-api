from database import *
from fastapi import FastAPI
from pydantic import BaseModel
from routers import harasser

app = FastAPI(title='Is They Harassing API', description='APIs for IsTheyHarassing.com', version='0.1')
app.include_router(harasser.router_harassers)

@app.get("/")
async def root():
    return {"message": "IsTheyHarassing API!"}


@app.on_event("startup")
async def startup():
    print("Connecting...")
    if conn.is_closed():
        conn.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()