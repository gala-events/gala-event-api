from uuid import UUID
from pydantic import BaseModel


class BaseVenue(BaseModel):
    name: str
    location: str


class VenueCreate(BaseVenue):
    max_capacity: int


class Venue(BaseVenue):
    id: UUID
    max_capacity: int
