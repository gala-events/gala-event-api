import re
from typing import List
from fastapi import APIRouter, Depends, Query
from models import Event, EventCreate
from uuid import uuid4
from db import Database, CRUD
from utils.db import get_db
routes = APIRouter()


@routes.post("/", response_model=Event)
def create_event(event: EventCreate, db=Depends(get_db)):
    event_id = CRUD.create(db, "events", event.dict())
    event_record = CRUD.find_by_id(db, "events", event_id)
    event = Event(**event_record)
    return event


@routes.get("/", response_model=List[Event])
def get_events(db=Depends(get_db),
               skip: int = 0,
               limit: int = 25,
               search: str = None,
               sort: List[str] = Query([], alias="sort_by")):
    filter_params = dict()
    search_fields = ["id", "name"]
    if search:
        map(lambda search_field: filter_params.update(
            search_field=re.compile(search)), search_fields)

    data = CRUD.find(db, "events", skip=skip,
                     limit=limit,
                     filter_params=filter_params,
                     sort=sort)
    return [Event(**d) for d in data]


@routes.put("/")
def update_events():
    pass


@routes.delete("/")
def delete_events():
    pass


@routes.get("/{event_id}")
def get_event(event_id: str):
    pass


@routes.put("/{event_id}")
def update_event(event_id: str):
    pass


@routes.patch("/{event_id}")
def partial_update_event(event_id: str):
    pass


@routes.delete("/{event_id}")
def delete_event(event_id: str):
    pass
