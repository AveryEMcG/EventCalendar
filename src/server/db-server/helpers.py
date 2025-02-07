import db
import datetime

SECONDS_IN_MINUTE = 60
SECONDS_IN_DAY = 86400

# we're also going to use some offsets
SUNDAY_SECONDS = 0 * SECONDS_IN_DAY
MONDAY_SECONDS = 1 * SECONDS_IN_DAY
TUESDAY_SECONDS = 2 * SECONDS_IN_DAY
WEDNESDAY_SECONDS = 3 * SECONDS_IN_DAY
THURSDAY_SECONDS = 4 * SECONDS_IN_DAY
FRIDAY_SECONDS = 5 * SECONDS_IN_DAY
SATURDAY_SECONDS = 6 * SECONDS_IN_DAY

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


def isOvernight(start, end):
    if end < start:
        return True
    return False


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


def timeIsUnique(newEvent, eventList):
    newEventStartTime = datetime.datetime.fromtimestamp(newEvent.start_time)
    newEventEndTime = datetime.datetime.fromtimestamp(
        (newEvent.start_time) + (newEvent.duration * SECONDS_IN_MINUTE)
    )

    for existingEvent in eventList:
        existingEventStartTime = datetime.datetime.fromtimestamp(
            existingEvent.start_time
        )
        existingEventEndTime = datetime.datetime.fromtimestamp(
            (existingEvent.start_time + existingEvent.duration * SECONDS_IN_MINUTE)
        )

        # See if the event conflicts with other events
        if collides(
            newEventStartTime,
            newEventEndTime,
            existingEventStartTime,
            existingEventEndTime,
        ):
            return False

        # 1 - get the absolute times (which is a second offset from midnight on a given day)
        newEventAbsoluteStart = getDayAgnosticMS(newEventStartTime)
        newEventAbsoluteEnd = newEventAbsoluteStart + (
            newEvent.duration * SECONDS_IN_MINUTE
        )

        existingEventAbsoluteStart = getDayAgnosticMS(existingEventStartTime)
        existingEventAbsoluteEnd = existingEventAbsoluteStart + (
            existingEvent.duration * SECONDS_IN_MINUTE
        )

        # 2-4 - make our projections
        newEventProjections = generateWeekProjection(
            newEvent, newEventAbsoluteStart, newEventAbsoluteEnd
        )
        existingEventsProjections = generateWeekProjection(
            existingEvent, existingEventAbsoluteStart, existingEventAbsoluteEnd
        )

        # we're going to insert the new event to the projection as well
        newEventProjections.append(
            (
                newEventAbsoluteStart + WEEK_SECONDS[newEventStartTime.weekday()],
                newEventAbsoluteEnd + WEEK_SECONDS[newEventStartTime.weekday()],
            )
        )
        existingEventsProjections.append(
            (
                existingEventAbsoluteStart
                + WEEK_SECONDS[existingEventStartTime.weekday()],
                existingEventAbsoluteEnd
                + WEEK_SECONDS[existingEventStartTime.weekday()],
            )
        )

        for projection1 in newEventProjections:
            for projection2 in existingEventsProjections:
                if collides(
                    projection1[0], projection1[1], projection2[0], projection2[1]
                ):
                    return False
    return True


def getDayAgnosticMS(date):
    return date.hour * 60 * 60 + (date.minute * 60) + (date.second)
