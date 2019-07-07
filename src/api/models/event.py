from typing import List, Union
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class FormAddress(BaseModel):
    line_1: str
    state: str
    country: str
    landmark: str
    zip_code: str
    geo_location_link: str


class GeoLocationAddress(BaseModel):
    latitude: str
    longitude: str


class GoogleAddress(BaseModel):
    url: str


class BaseEvent(BaseModel):
    name: str
    description: str

    start: datetime
    end: datetime

    location: Union[FormAddress, GeoLocationAddress, GoogleAddress]
    owner: UUID

    tags: List[str]
    private: bool


class EventCreate(BaseEvent):
    pass


class Event(BaseEvent):
    uuid: UUID
