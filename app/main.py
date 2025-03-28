from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI
from api.events import router as event_router
from api.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(event_router, prefix="/api/events")


@app.get("/")
def read_root():
    return {"Hello": "My World"}


@app.get("/items/{id}")
def read_item(id: int, q: Union[str, None] = None):
    return {"item_id": id, "q": q}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
