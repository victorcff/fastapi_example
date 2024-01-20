import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import get_async_pool, get_pool
from app.routers import student

def startup():
  asyncio.create_task(check_connections())
  asyncio.create_task(check_async_connections())

@asynccontextmanager
async def lifespan(app: FastAPI):
  startup()
  yield

app = FastAPI(lifespan=lifespan)

pool = get_pool()
async_pool = get_async_pool()

app.include_router(student.router)

async def check_connections():
  while True:
    await asyncio.sleep(600)
    print("Check Connections")
    pool.check()
    
async def check_async_connections():
  while True:
    await asyncio.sleep(600)
    print("Check Async Connections")
    await async_pool.check()

@app.get("/")
async def Home():
  return "Welcome Home"