import { ScheduledEvent } from "./Events";
import { useState } from "react";
import toast, { Toaster } from 'react-hot-toast';
import "react-datepicker/dist/react-datepicker.css";



function isClientError(statusCode : number) {
    return statusCode >= 400 && statusCode < 500;
  }
function isServerError(statusCode : number) {
    return statusCode >= 500 && statusCode < 600;
  }

export function AddEventBox(props:any){
    const [startDate, setStartDate] = useState(new Date());
    const [repeatsSunday, setRepeatsSunday] = useState(false);
    const [repeatsMonday, setRepeatsMonday] = useState(false);
    const [repeatsTuesday, setRepeatsTuesday] = useState(false);
    const [repeatsWednesday, setRepeatsWednesday] = useState(false);
    const [repeatsThursday, setRepeatsThursday] = useState(false);
    const [repeatsFriday, setRepeatsFriday] = useState(false);
    const [repeatsSaturday, setRepeatsSaturday] = useState(false);
    const [duration,setDuration]=useState(0)
    
    const handleSubmit = (event: any) => {
        event.preventDefault(); 

        var body: ScheduledEvent= {
            name:"n/a",
            id:0,
            duration:duration,
            //This is annoying, but the calendar needs seconds and valueof gives ms
            start_time: startDate.valueOf()/1000, 
            repeats_su:repeatsSunday,
            repeats_m:repeatsMonday,
            repeats_t:repeatsTuesday,
            repeats_w:repeatsWednesday,
            repeats_th:repeatsThursday,
            repeats_f:repeatsFriday,
            repeats_s:repeatsSaturday,
        }

        //Try to post the event
        fetch(props.backend_url+"/events", {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({body
            })
          }).then((resp)=>{
            //give toasts based on response
            if (isClientError(resp.status)){
                resp.json().then((err)=> {
                  toast.error("Error in adding event: "+err.detail)}
                )
                return
            }
            if (isServerError(resp.status)){
                toast.error("Server error in adding event")
                return
            }
            if ((resp.status)==200){
                toast.success("Successfully added event, refresh page to see changes!")
                return
            }
            toast("Got back response code: " + resp.status)
            
        })
          
       
        // Your custom form handling logic here
      };
  return (

    <>
    <form onSubmit={handleSubmit}>
    <input aria-label="Date and time" type="datetime-local" onChange={(event)=>setStartDate(new Date(event.target.value))}/>   <br/>
    Duration(Minutes, 1 or more):<input type="number"onChange={(event)=>setDuration(Number(event.target.value))}/><br/>
    Repeats Sunday: <input type="Checkbox" onChange={(event)=>setRepeatsSunday(event.target.checked)}/><br/>
    Repeats Monday: <input type="Checkbox"onChange={(event)=>setRepeatsMonday(event.target.checked)}/><br/>
    Repeats Tuesday: <input type="Checkbox"onChange={(event)=>setRepeatsTuesday(event.target.checked)}/><br/>
    Repeats Wednesday: <input type="Checkbox"onChange={(event)=>setRepeatsWednesday(event.target.checked)}/><br/>
    Repeats Thursday: <input type="Checkbox"onChange={(event)=>setRepeatsThursday(event.target.checked)}/><br/>
    Repeats Friday: <input type="Checkbox"onChange={(event)=>setRepeatsFriday(event.target.checked)}/><br/>
    Repeats Saturday: <input type="Checkbox"onChange={(event)=>setRepeatsSaturday(event.target.checked)}/><br/>

    <input type="submit"value="Create New Event"/></form>
    <Toaster/>
    </>
  )

}