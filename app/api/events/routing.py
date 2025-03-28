from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .models import EventModel, EventListSchema, EventCreateSchema, EventUpdateSchema
from api.db.session import get_session

router = APIRouter()


@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    query = select(EventModel).order_by(EventModel.id.desc()).limit(10)
    results = session.exec(query).all()

    return {"results": results, "count": len(results)}


@router.post("/")
def create_event(
    payload: EventCreateSchema, session: Session = Depends(get_session)
) -> EventModel:
    data = payload.model_dump()
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.get("/{event_id}")
def get_event(event_id: int, session: Session = Depends(get_session)) -> EventModel:
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Event with id: {event_id} was not found"
        )
    return result


@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateSchema) -> EventModel:
    data = payload.model_dump()
