from typing import List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from .venue import Venue


class BaseEvent(BaseModel):
    name: str
    scheduled_on: datetime = datetime.now()
    capacity: int
    venues: List[Venue] = []


class EventCreate(BaseEvent):
    pass


class Event(BaseEvent):
    id: UUID
