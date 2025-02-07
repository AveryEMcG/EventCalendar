from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import db
import helpers
from pydantic import BaseModel

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

#{"body":{"name":"n/a","id":0,"duration":100,"start_time":1739031060,"repeats_su":false,"repeats_m":false,"repeats_t":false,"repeats_w":false,"repeats_th":false,"repeats_f":false,"repeats_s":false}}

class Event_Struct(BaseModel):
    name: str
    start_time: int
    duration: int
    repeats_su: int
    repeats_m: int
    repeats_t: int
    repeats_w: int
    repeats_th: int
    repeats_f: int
    repeats_s: int

class Body(BaseModel):
    body: Event_Struct

def eventStructToDBEvent(newEvent):
      return db.Event(None, newEvent["name"],newEvent["start_time"],newEvent["duration"],newEvent["repeats_su"],newEvent["repeats_m"],newEvent["repeats_t"],newEvent["repeats_w"],newEvent["repeats_th"],newEvent["repeats_f"],newEvent["repeats_s"])


@app.get("/events")
def get_events():
    response = db.query("SELECT * FROM ScheduledEvents")
    return jsonable_encoder(response)


@app.post("/events")
async def create_event(event: Body):
        event_dict = event.body.model_dump()
        newDbEvent = eventStructToDBEvent(event_dict)
        eventList = db.query("SELECT * FROM ScheduledEvents")
        if(helpers.timeIsUnique(newDbEvent,eventList)):
                result = db.insert("INSERT INTO ScheduledEvents VALUES (NULL,\""+str(event_dict["name"])+"\","+str(event_dict["start_time"])+","+str(event_dict["duration"])+","+str(event_dict["repeats_su"])+","+str(event_dict["repeats_m"])+","+str(event_dict["repeats_t"])+","+str(event_dict["repeats_w"])+","+str(event_dict["repeats_th"])+","+str(event_dict["repeats_f"])+","+str(event_dict["repeats_s"])+")")
        else:
                raise HTTPException(status_code=400, detail="An event already exists at the time specified")
        return result
