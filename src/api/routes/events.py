import re
from typing import List, Dict
from fastapi import APIRouter, Depends, Query, Body
from pydantic import BaseModel
from models import Event, EventCreate
from uuid import uuid4
from db import Database, CRUD
from utils.db import get_db
routes = APIRouter()


@routes.post("/events", response_model=Event)
def create_event(event: EventCreate, db=Depends(get_db)):
    event_id = CRUD.create(db, "events", event.dict())
    event_record = CRUD.find_by_uuid(db, "events", event_id)
    event = Event(**event_record)
    return event


@routes.get("/events", response_model=List[Event])
def get_events(db=Depends(get_db),
               skip: int = 0,
               limit: int = 25,
               search: str = None,
               sort: List[str] = Query([], alias="sort_by")):
    filter_params = dict()
    search_fields = ["uuid", "name"]
    if search:
        map(lambda search_field: filter_params.update(
            search_field=re.compile(search)), search_fields)

    data = CRUD.find(db, "events", skip=skip,
                     limit=limit,
                     filter_params=filter_params,
                     sort=sort)
    return [Event(**d) for d in data]


@routes.get("/events/{event_id}", response_model=Event)
def get_event(event_id: str, db=Depends(get_db)):
    data = CRUD.find_by_uuid(db, "events", event_id)
    return Event(**data)


@routes.put("/events/{event_id}", response_model=Event)
def update_event(event_id: str, event: EventCreate, db=Depends(get_db)):
    data = CRUD.update(db, "events", event_id, event.dict())
    return Event(**data)


@routes.patch("/events/{event_id}", response_model=Event)
def partial_update_event(event_id: str, event=Body(...), db=Depends(get_db)):
    data = CRUD.update(db, "events", event_id, event.dict())
    return Event(**data)


@routes.delete("/events/{event_id}")
def delete_event(event_id: str, db=Depends(get_db)):
    CRUD.delete(db, "events", event_id)
    return dict(message="Event deleted successfully")
