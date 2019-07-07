import re
from os.path import join
from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, Body, Depends, Query
from pydantic import BaseModel
from starlette.responses import JSONResponse, Response
from starlette.status import (HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                              HTTP_404_NOT_FOUND)

from db import CRUD, Database
from models import Event, EventCreate
from utils import get_db, json_merge_patch
from utils.exceptions import RecordNotFoundException

routes = APIRouter()


@routes.post("/events", response_model=Event)
def create_event(event: EventCreate, db=Depends(get_db)):
    event_id = CRUD.create(db, "events", event.dict())
    event_record = CRUD.find_by_uuid(db, "events", str(event_id))
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
def update_event(event_id: str, event: Event, response: Response, db=Depends(get_db)):
    try:
        data = CRUD.update(db, "events", event_id, event.dict())
        return Event(**data)
    except RecordNotFoundException as exc:
        response.status_code = HTTP_404_NOT_FOUND
        return JSONResponse(dict(error=str(exc)))
    except:
        response.status_code = HTTP_400_BAD_REQUEST
        return JSONResponse(dict(error="Failed to update %s record" % event_id))


@routes.patch("/events/{event_id}", response_model=Event)
def partial_update_event(event_id: str, event: Dict, db=Depends(get_db)):
    existing_event = CRUD.find_by_uuid(db, "events", event_id)
    updated_event = json_merge_patch(
        existing_event, event)
    data = CRUD.update(db, "events", event_id, updated_event)
    return Event(**data)


@routes.delete("/events/{event_id}", response_model=BaseModel)
def delete_event(event_id: str, response: Response, db=Depends(get_db)):
    try:
        CRUD.delete(db, "events", event_id)
        response.status_code = HTTP_204_NO_CONTENT
        return JSONResponse(dict(message="Event %s deleted successfully." % event_id))
    except RecordNotFoundException as exc:
        response.status_code = HTTP_404_NOT_FOUND
        return JSONResponse(dict(error=str(exc)))
    except:
        response.status_code = HTTP_400_BAD_REQUEST
        return JSONResponse(dict(error="Failed to delete Event %s." % event_id))
