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
const [dateRange, setDateRange]= useState<Date[]>(initalizeDateRange())

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