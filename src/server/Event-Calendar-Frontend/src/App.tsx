import { useState } from 'react'
import { Calendar, dateFnsLocalizer} from 'react-big-calendar'
import format from 'date-fns/format'
import parse from 'date-fns/parse'
import startOfWeek from 'date-fns/startOfWeek'
import getDay from 'date-fns/getDay'
import enUS from 'date-fns/locale/en-US'
import addHours from 'date-fns/addHours'


import './App.css'
import 'react-big-calendar/lib/addons/dragAndDrop/styles.css'
import 'react-big-calendar/lib/css/react-big-calendar.css'


// This is our database representation of scheduled events, 
// we'll need to transform it to be used by react-big-calendar
interface ScheduledEvent {
  name: string;
  id: number;
  start_time: Date;
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
interface Event {
  name: string;
  id: number;
  start: Date;
  end: Date;
}

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

function App() {
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

  // when we click through the weeks in the calendar, update our internal state
  const onRangeChange = data => {setDateRange(data)}

  return (
    <Calendar
      defaultView='week'
      events={[]}
      onRangeChange={onRangeChange}
      localizer={localizer}
      style={{ height: '100vh' }}
    />
  )
}

export default App