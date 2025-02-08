# EventCalendar
 A calendar to view Scheduled Events

## Overview: 

In this service, there exists a series of events which have a start time and duration, may repeat, but never conflict in time.
Users can add events to the calendar using the date input fields on the page.

### Front end: 
react JS via [VITE](https://vite.dev/), using the following packages:
* [react-big-calendar](https://www.npmjs.com/package/react-big-calendar) - a nice big friendly calendar to display the events on 
* [react-hot-toast](https://react-hot-toast.com/) - simple toasting feature

### Back end: 
Python server using [FAST API](https://fastapi.tiangolo.com/),connected to a [SQLite](https://www.sqlite.org/index.html) database

## Installing + Running

### Install Commands:
From src/server/db-server:
* Create a virtualenv
```
python -m venv .venv
source .venv/bin/activate
```
* Then you can run:
```
pip install -r requirements.txt
```
* Then navigate to Event-Calendar-Frontend and run:
```
npm install
```

### Running
* From one terminal - navigate to /src/server/Event-Calendar-Frontend and run :
```
npm run dev
```
* From another terminal - navigate to /src/server/db-server and run:
```
fastapi dev main.py
```

## Troubleshooting
* The URL for the backend server is stored in src/server/Event-Calendar-Frontend/App.tsx, if for some reason FastAPI doesn't launch on the default IP/port, you can copy and paste the address to the ``BACKEND_URL`` variable.

## Assumptions / Notes:
* Users are trusted and auth isn't necessary
* Only 1 user may be using the service at once (I did not include a semaphore locking gate around the database read/writes)
* Users do not need a UI to modify, delete, or view details of the event. (But I included fields to make this possible in the future - all events have an ID and name such that they can be viewed + retrieved in a human friendly way!)
* Users will stay on the 'week' view of the UI. (If this were to go live in production, I would remove the other views)
* Users will not fill in data fields with garbage like negative times (this too should be cleaned up before going live - but there is some data validation in place already automatically)
* Users must refresh page to get newest data, auto-refresh should be implemented before rolling to production.
* The database comes pre-populated with some events
* Overnight events are displayed by the calendar module as lines at the top of the screen - this can be confusing
* Various other smaller misc TODOs marked in-place in the code
