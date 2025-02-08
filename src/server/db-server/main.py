from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import db
import helpers
from pydantic import BaseModel

# -- Defines + Headers -- #
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# These are the data types we'll be getting over the wire
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

# -- Helper Functions -- #

# This converts from JSON to our internal data formatting
def eventStructToDBEvent(newEvent):
    # we always leave the ID field void so sqlite will populate it appropriately
    return db.Event(
        None,
        newEvent["name"],
        newEvent["start_time"],
        newEvent["duration"],
        newEvent["repeats_su"],
        newEvent["repeats_m"],
        newEvent["repeats_t"],
        newEvent["repeats_w"],
        newEvent["repeats_th"],
        newEvent["repeats_f"],
        newEvent["repeats_s"],
    )


def insertDBDataFromDict(event_dict):
        #TODO: This is messy, clean it up
        db.insert(
            'INSERT INTO ScheduledEvents VALUES (NULL,"'
            + str(event_dict["name"])
            + '",'
            + str(event_dict["start_time"])
            + ","
            + str(event_dict["duration"])
            + ","
            + str(event_dict["repeats_su"])
            + ","
            + str(event_dict["repeats_m"])
            + ","
            + str(event_dict["repeats_t"])
            + ","
            + str(event_dict["repeats_w"])
            + ","
            + str(event_dict["repeats_th"])
            + ","
            + str(event_dict["repeats_f"])
            + ","
            + str(event_dict["repeats_s"])
            + ")"
        )

# -- API -- #
@app.get("/events")
def get_events():
    response = db.query("SELECT * FROM ScheduledEvents")
    return jsonable_encoder(response)


@app.post("/events")
async def create_event(event: Body):
    # convert the data over
    event_dict = event.body.model_dump()
    newDbEvent = eventStructToDBEvent(event_dict)

    # get our existing events
    eventList = db.query("SELECT * FROM ScheduledEvents")

    # make sure we aren't going to have an overlapping event
    if helpers.timeIsUnique(newDbEvent, eventList):

        # this is messy, it should be moved into a new function
        result = insertDBDataFromDict(event_dict)

    # let the user know there is a conflict
    else:
        raise HTTPException(
            status_code=400, detail="An event already exists at the time specified"
        )

    return result
