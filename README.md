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
To get the front-end dependencies installed properly:
* navigate to Event-Calendar-Frontend and run:
```
npm install
```

### Running
* From one terminal - launch the front end located in /src/server/Event-Calendar-Frontend:
`` npm run dev``
* From another terminal - launch the back end via fastapi:
``fastapi dev main.py``

## Assumptions / Notes:
* Users are trusted and auth isn't necessary
* Only 1 user may be using the service at once (I did not include a semaphore locking gate around the database read/writes)
* Users do not need a UI to modify, delete, or view details of the event. (But I included fields to make this possible in the future - all events have an ID and name such that they can be viewed + retrieved in a human friendly way!)
* Users will stay on the 'week' view of the UI. (If this were to go live in production, I would remove the other views)
* Users will not fill in data fields with garbage like negative times (this too should be cleaned up before going live - but there is some data validation in place already automatically)
* Users must refresh page to get newest data, auto-refresh should be implemented before rolling to production.
* The database comes pre-populated with some events
* Overnight events are displayed by the calendar module as lines at the top of the screen - this can be confusing

