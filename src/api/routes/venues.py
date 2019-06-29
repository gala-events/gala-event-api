from fastapi import APIRouter

routes = APIRouter()


@routes.post("/")
def create_venue():
    pass


@routes.get("/")
def get_venues():
    pass


@routes.put("/")
def update_venues():
    pass


@routes.delete("/")
def delete_venues():
    pass


@routes.get("/{venue_id}")
def get_venue(venue_id: str):
    pass


@routes.put("/{venue_id}")
def update_venue(venue_id: str):
    pass


@routes.patch("/{venue_id}")
def partial_update_venue(venue_id: str):
    pass


@routes.delete("/{venue_id}")
def delete_venue(venue_id: str):
    pass
