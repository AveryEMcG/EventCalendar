import { useState, useEffect } from 'react'
import { Calendar, dateFnsLocalizer} from 'react-big-calendar'
import format from 'date-fns/format'
import parse from 'date-fns/parse'
import startOfWeek from 'date-fns/startOfWeek'
import getDay from 'date-fns/getDay'
import enUS from 'date-fns/locale/en-US'
import addHours from 'date-fns/addHours'
import 'react-big-calendar/lib/addons/dragAndDrop/styles.css'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import { ScheduledEvent,ConvertServerEvents } from './Events'
const BACKEND_URL = "http://127.0.0.1:8000"
//grabs a series of the 0th hour from the past week. Necessary to pre-populate date range
function initalizeDateRange(){
  let curr = new Date 
  let week = []
  
  let day = startOfWeek(curr)
  week.push(day)
  for (let i = 0; i <= 6; i++) {
    day = addHours(day,24)
    week.push(day)
  }
  return week
}

export function EventCalendar(props: any) {
const [events, setEvents] = useState<ScheduledEvent[]>([])
const [dateRange, setDateRange]= useState<Date[]>(initalizeDateRange())

// necessary init data for proper calendar localization
const locales = {
  'en-US': enUS,
}
  const localizer = dateFnsLocalizer({
    format,
    parse,
    startOfWeek,
    getDay,
    locales,
  })

  //On mount, let's grab the current database
  useEffect(() => { 
    fetch(props.backend_url+"/events").then((resp)=>{
      return resp.json()
     }).then((eventsList)=>{
      setEvents(eventsList)
     });
   }, [])

   console.log(events)
  


  // when we click through the weeks in the calendar, update our internal state
  const onRangeChange = data => {setDateRange(data)}
  const calenderEvents = ConvertServerEvents(events, dateRange)

  return (
    <Calendar
      defaultView='week'
      events={calenderEvents}
      onRangeChange={onRangeChange}
      localizer={localizer}
      style={{ height: '100vh' }}
    />
  )
}

