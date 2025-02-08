import db
import datetime

# ---- Globals ----
# Defining some times here, we'll use them in our calculations below:
SECONDS_IN_MINUTE = 60
SECONDS_IN_DAY = 86400

# we're also going to use some offsets into a week
MONDAY_SECONDS = 0 * SECONDS_IN_DAY
TUESDAY_SECONDS = 1 * SECONDS_IN_DAY
WEDNESDAY_SECONDS = 2 * SECONDS_IN_DAY
THURSDAY_SECONDS = 3 * SECONDS_IN_DAY
FRIDAY_SECONDS = 4 * SECONDS_IN_DAY
SATURDAY_SECONDS = 5 * SECONDS_IN_DAY
SUNDAY_SECONDS = 6 * SECONDS_IN_DAY

# python does weekdays starting on Monday
WEEK_SECONDS = [
    MONDAY_SECONDS,
    TUESDAY_SECONDS,
    WEDNESDAY_SECONDS,
    THURSDAY_SECONDS,
    FRIDAY_SECONDS,
    SATURDAY_SECONDS,
    SUNDAY_SECONDS,
]


# ---- Small Helper functions  ----
# events have duration and start time, this makes getting the end time easier in-line
def getEndTimeForEvent(event):
    return (event.start_time) + (event.duration * SECONDS_IN_MINUTE)


# Check if an event is repeating
def isRepeating(event):
    if event.repeats_su:
        return True
    if event.repeats_m:
        return True
    if event.repeats_t:
        return True
    if event.repeats_w:
        return True
    if event.repeats_th:
        return True
    if event.repeats_f:
        return True
    if event.repeats_s:
        return True
    return False


# Find out how many seconds from a date until a day of the week. This is NOT a good way to solve this.
# TODO: find a better way to do this
def addUntilDay(date, day):
    days = 0
    while date.weekday() + days * SECONDS_IN_DAY < day:
        days + 1
    return days * SECONDS_IN_DAY


# get how many MS a date is into that day
def getDayAgnosticMS(date):
    return date.hour * 60 * 60 + (date.minute * 60) + (date.second)


# Check if two windows of time are intersecting
def collides(start1, end1, start2, end2):
    first = None
    second = None

    # if the events happen at the same time, there's collision
    if start1 == start2:
        return True

    # find out which event happens first
    if start1 > start2:
        first = (start2, end2)
        second = (start1, end1)
    else:
        first = (start1, end1)
        second = (start2, end2)

    # if the first event ends before the second one starts, there's collision
    if first[1] > second[0]:
        return True
    return False


#  --- Projections ---
# Takes a event, and returns a list of subsequent start/stop times for 1 week AFTER the initial event
def generateFirstWeekProjection(event, start, end):
    startDate = datetime.datetime.fromtimestamp(start)
    projections = []
    if event.repeats_su == 1:
        offset = addUntilDay(startDate, 6)
        projections.append((start + offset, end + offset))
    if event.repeats_m == 1:
        offset = addUntilDay(startDate, 0)
        projections.append((start + offset, end + offset))
    if event.repeats_t == 1:
        offset = addUntilDay(startDate, 1)
        projections.append((start + offset, end + offset))
    if event.repeats_w == 1:
        offset = addUntilDay(startDate, 2)
        projections.append((start + offset, end + offset))
    if event.repeats_th == 1:
        offset = addUntilDay(startDate, 3)
        projections.append((start + offset, end + offset))
    if event.repeats_f == 1:
        offset = addUntilDay(startDate, 4)
        projections.append((start + offset, end + offset))
    if event.repeats_s == 1:
        offset = addUntilDay(startDate, 5)
        projections.append((start + offset, end + offset))
    return projections


# Takes a event, and returns a list of start/stop times for 1 week
def generateWeekProjection(event, absoluteStart, absoluteEnd):
    projections = []
    if event.repeats_su == 1:
        projections.append(
            (absoluteStart + SUNDAY_SECONDS, absoluteEnd + SUNDAY_SECONDS)
        )
    if event.repeats_m == 1:
        projections.append(
            (absoluteStart + MONDAY_SECONDS, absoluteEnd + MONDAY_SECONDS)
        )
    if event.repeats_t == 1:
        projections.append(
            (absoluteStart + TUESDAY_SECONDS, absoluteEnd + TUESDAY_SECONDS)
        )
    if event.repeats_w == 1:
        projections.append(
            (absoluteStart + WEDNESDAY_SECONDS, absoluteEnd + WEDNESDAY_SECONDS)
        )
    if event.repeats_th == 1:
        projections.append(
            (absoluteStart + THURSDAY_SECONDS, absoluteEnd + THURSDAY_SECONDS)
        )
    if event.repeats_f == 1:
        projections.append(
            (absoluteStart + FRIDAY_SECONDS, absoluteEnd + FRIDAY_SECONDS)
        )
    if event.repeats_s == 1:
        projections.append(
            (absoluteStart + SATURDAY_SECONDS, absoluteEnd + SATURDAY_SECONDS)
        )
    return projections


#  --- Detailed Collision Detection Logic --- #


# Check if two events in isolation (no repeats) collide with one another
def eventsCollide(existingEvent, newEvent):
    if collides(
        newEvent.start_time,
        getEndTimeForEvent(newEvent),
        existingEvent.start_time,
        getEndTimeForEvent(existingEvent),
    ):
        return True


# Check if there's collisions for the first event (sans its repeats)
def firstWeekCollides(event, newEvent):
    # project out a week from the exisiting event
    week = generateFirstWeekProjection(
        event, event.start_time, getEndTimeForEvent(event)
    )
    for w in week:
        # if that repeating event is AFTER or INTERSECTS that event, double check whether it collides
        if newEvent.start_time >= w[1]:
            if collides(w[0], w[1], newEvent.start_time, getEndTimeForEvent(newEvent)):
                return True
    return False


# Checks if repeats of either a new or existing event can conflict
def repeatsCollide(newEvent, existingEvent):
    existingEventStartTime = datetime.datetime.fromtimestamp(existingEvent.start_time)
    newEventStartTime = datetime.datetime.fromtimestamp(newEvent.start_time)

    # Get 'absolute' times - these are offsets from midnight in second
    newEventAbsoluteStart = getDayAgnosticMS(newEventStartTime)
    newEventAbsoluteEnd = newEventAbsoluteStart + (
        newEvent.duration * SECONDS_IN_MINUTE
    )
    existingEventAbsoluteStart = getDayAgnosticMS(existingEventStartTime)
    existingEventAbsoluteEnd = existingEventAbsoluteStart + (
        existingEvent.duration * SECONDS_IN_MINUTE
    )

    # Project out those absolute times for all days to be repeated
    newEventProjections = generateWeekProjection(
        newEvent, newEventAbsoluteStart, newEventAbsoluteEnd
    )
    existingEventsProjections = generateWeekProjection(
        existingEvent, existingEventAbsoluteStart, existingEventAbsoluteEnd
    )

    # Compare these projections and see if there are any conflicts
    for projection1 in newEventProjections:
        for projection2 in existingEventsProjections:
            if collides(projection1[0], projection1[1], projection2[0], projection2[1]):
                return True
    return False


# Checks if time is unique. Relies on the functions above!
def timeIsUnique(newEvent, eventList):
    for existingEvent in eventList:
        if eventsCollide(newEvent=newEvent, existingEvent=existingEvent):
            return False
        if firstWeekCollides(newEvent, existingEvent):
            return False
        if repeatsCollide(newEvent=newEvent, existingEvent=existingEvent):
            return False
    return True
