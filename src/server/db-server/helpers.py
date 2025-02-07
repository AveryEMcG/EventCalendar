import db
import datetime

SECONDS_IN_MINUTE = 60

def isOvernight(start,end):
    if end<start:
        return True
    return False



def timeIsUnique(newEvent):
    eventList = db.query("SELECT * FROM ScheduledEvents")
    newEventStartTime = datetime.datetime.fromtimestamp(newEvent["start_time"])
    newEventEndTime = datetime.datetime.fromtimestamp((newEvent["start_time"])+(newEvent["duration"]*SECONDS_IN_MINUTE))

    for e in eventList:

        eventStartTime = datetime.datetime.fromtimestamp(e.start_time)
        eventEndTime = datetime.datetime.fromtimestamp((e.start_time+e.duration*SECONDS_IN_MINUTE))
        
        #check if the absolute time is colliding
        if isColliding(newEventStartTime,newEventEndTime,eventStartTime,eventEndTime):

            return False
        print("Passed Check 1, going to check 2")

        # Now we'll check for repeating events
        # first, are they occurring at the same time of day?
        agnosticNewEventStart = getDayAgnosticMS(newEventStartTime)
        agnosticNewEventEnd = getDayAgnosticMS(newEventEndTime)
        agnosticExistingEventStart = getDayAgnosticMS(eventStartTime)
        agnosticExistingEventEnd = getDayAgnosticMS(eventEndTime)

        if currentlyCollides(agnosticNewEventStart,agnosticNewEventEnd,agnosticExistingEventStart,agnosticExistingEventEnd):


            #if they're at the same time of day, they risk overlapping for day repeats.
            #let's check! :)

            #We need to check if they repeat on the same day, OR if there's a repeat
            if (newEvent["repeats_su"] ==1):
                if (e.repeats_su ==1):
                    return False
                if (eventStartTime.weekday() ==0):
                    return False

            if (newEvent["repeats_m"] ==1): 
                if(e.repeats_m ==1):
                    return False
                if (eventStartTime.weekday() ==1):
                    return False
            
            if (newEvent["repeats_t"] ==1):
                if (e.repeats_t ==1):
                    return False
                if (eventStartTime.weekday() ==2):
                    return False
            
            if (newEvent["repeats_w"] ==1):
                if(e.repeats_w ==1):
                    return False
                if(eventStartTime.weekday() ==3):
                    return False
                        
            if (newEvent["repeats_th"] ==1):
                if(e.repeats_th ==1):
                    return False
                if(eventStartTime.weekday() ==4):
                    return False
            
            if (newEvent["repeats_f"] ==1):
                if(e.repeats_f ==1):
                    return False
                if(eventStartTime.weekday() ==5):
                    return False        
                                
            if (newEvent["repeats_s"] ==1):
                if(e.repeats_s ==1):
                    return False
                if(eventStartTime.weekday() ==6):
                    return False     
                                         
    #if it didn't happen yet, we're good :)
    print ("not colliding at all!")
    return True
    
def currentlyCollides(start1,end1, start2,end2):

    first = None
    second = None
    
    # if the events happen at the same time, there's collision
    if (start1==start2):
        return True
    
    #find out which event happens first
    if (start1>start2):
        first = (start2,end2)
        second = (start1,end1)       
    else:
        first = (start1,end1)
        second = (start2,end2)     

    #if the first event ends before the second one starts, there's collision
    if (first[1]>second[0]):
        return True

    return False

def getDayAgnosticMS(date):
    return date.hour*1000*60*60+(date.minute*1000*60)+(date.second*1000)




def CurrentlyCollides(event1Start,event1End, event2Start,event2End):
    return False

def newEventRepeatsCollidesOnExistingEvent(event1Start,event1End, event1DayOfWeek, event2Start,event2End,event2DayOfWeek):
    return False

def newEventCollidesOnExistingEventRepeats(event1Start,event1End, event1DayOfWeek, event2Start,event2End,event2DayOfWeek):
    return False

def newEventRepeatsCollidesOnExistingEventRepeats(event1Start,event1End, event1DayOfWeek, event2Start,event2End,event2DayOfWeek):
    return False
