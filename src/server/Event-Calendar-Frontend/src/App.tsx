
import { EventCalendar } from "./components/EventCalendar"
import { AddEventBox } from "./components/AddEventBox"
import './App.css'

const BACKEND_URL = "http://127.0.0.1:8000"

function App() {
  return (
    <div className="main">
    <div className="calendar"><EventCalendar backend_url={BACKEND_URL}/></div>
    <div className="buttons"><AddEventBox backend_url={BACKEND_URL}/> </div>
    </div>
  )
}

export default App