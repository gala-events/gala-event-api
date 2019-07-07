import os
from fastapi import FastAPI, Depends
from starlette.requests import Request
from starlette.responses import Response
from routes import events
from db import Database
from pymongo import MongoClient
from utils import get_db

MONGO_DB__HOST_URI = os.environ.get("MONGO_DB__HOST_URI", "localhost")
MONGO_DB__HOST_PORT = int(os.environ.get("MONGO_DB__HOST_PORT", 27017))
db_connection = MongoClient(host=MONGO_DB__HOST_URI, port=MONGO_DB__HOST_PORT)

app = FastAPI(title="GALA Event Management API",
              description="Management module for performing REST operations on GALA event resources",
              openapi_url="/gala_event_api__openapi.json",
              version="v1")


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
                   prefix="/api/v1", tags=["CRUD on Events"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
