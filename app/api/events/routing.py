import os
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_events():
    print(os.environ.get("DATABASE_URL"))
    return {"items": [1, 2, 3]}
