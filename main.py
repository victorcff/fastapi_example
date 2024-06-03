from fastapi import FastAPI
from app.routers.feeder_devices import feeder_devices_router
from app.routers.meals import meals_router
from app.routers.users import users_router
from app.database.db import engine, Base
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8081, reload=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(feeder_devices_router)
app.include_router(meals_router)
app.include_router(users_router)