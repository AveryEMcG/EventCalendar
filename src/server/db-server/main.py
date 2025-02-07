from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import db


app = FastAPI()
origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/events")
def get_events():
    response = db.query("SELECT * FROM ScheduledEvents")
    return jsonable_encoder(response)


@app.post("/events")
async def create_event():
    return

  