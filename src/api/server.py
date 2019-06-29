from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import Response
from routes import events
from routes import venues
from db import Database
from pymongo import MongoClient
from utils.db import get_db

db_connection = MongoClient(host="localhost", port=27017)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = Database(db_connection)
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(events.routes,
                   prefix="/events", tags=["events"])
app.include_router(venues.routes, prefix="/venues", tags=["venues"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
