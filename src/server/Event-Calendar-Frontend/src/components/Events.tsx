import getDay from 'date-fns/getDay'
import addMilliseconds from 'date-fns/addMilliseconds'
import {  intervalToDuration } from 'date-fns'
import startOfDay from 'date-fns/startOfDay'
import {add} from 'date-fns/add'
import addHours from 'date-fns/addHours'


// This is our database representation of scheduled events, 
// we'll need to transform it to be used by react-big-calendar
export interface ScheduledEvent {
  name: string;
  id: number;
  start_time: number;
  duration: number;
  repeats_m: boolean;
  repeats_t: boolean;
  repeats_w: boolean;
  repeats_th: boolean; 
  repeats_f: boolean;    
  repeats_s: boolean;  
  repeats_su: boolean;  
}

// This is the react-big-calendar event
export interface Event {
  name: string;
  start: Date;
  end: Date;
}

export function isRepeating(event: any, day:Date):boolean{
  let dayOfWeek = getDay(day)
   
   switch(dayOfWeek){
     case(0):
       return(1==event.repeats_su)
     case(1):
       return (1==event.repeats_m)
     case(2):
       return (1==event.repeats_t)
     case(3):
       return (1==event.repeats_w)
     case(4):
       return (1==event.repeats_th)
     case(5):
       return (1==event.repeats_f)
     case(6):
       return (1==event.repeats_s)
   }
   return false
}

export function ConvertServerEvents(events:any, dateRange:Date[]): Event[]{
  console.log(dateRange)
  var eventList = []
  for (let i = 0; i<events.length; i++){
     if(events[i].start_time<addHours(dateRange[6],24)){
     
      let eventTimeSeconds = events[i].start_time*1000
      let eventDate = new Date(eventTimeSeconds)
      let eventEnd = addMilliseconds(eventDate,(events[i].duration*1000*60))
      console.log(eventDate, " is the start time of event ", events[i].id," and this is the end-> ",eventEnd)

      eventList.push( {name: events[i].name,
           start: eventDate,
           end:  eventEnd})
      for (let d = 0; d<dateRange.length; d++){

        if (isRepeating(events[i], dateRange[d])){
         
          let newTimeOffset = intervalToDuration({start:startOfDay(eventDate), end: eventDate})

          let newEventDate = add(dateRange[d],newTimeOffset)

          if (newEventDate>eventDate){
            eventList.push( {name: events[i].name,
              start: newEventDate,
              end: addMilliseconds(newEventDate,events[i].duration*1000*60)           
          })
        }
          else{
            console.log("didn't add event, repeats before start time")

          }

        }
      }

     }
  }

  console.log(eventList)
  return eventList

  }
