const express = require('express')

//Connecting to supabase
const {createClient} = require('@supabase/supabase-js')
const supabase = createClient('https://pjshkjaswzdtfuxpqxfr.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqc2hramFzd3pkdGZ1eHBxeGZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc1NjEzNjEsImV4cCI6MjAxMzEzNzM2MX0.t_oXV-0P24Z1oFebdvzAdG-ujrN8vfJP1J2tbRlbkpk')

const app = express.Router()

async function getSpecificEvent(id){
    let { data: event, error } = await supabase
        .from('events')
        .select('*')
        .eq('id',id)
    if(error){
        console.log(error)
    }else{
        return event
    }
}

//Render page editEvent.ejs when user clicks the Edit button
app.get('/editevent',async (req, res) => {
    const event = await getSpecificEvent(req.query.eventid)
    return res.render('editEvent',{
        row:event
    })
})

//Update changes in the event details
app.post('/editevent',async (req, res)=>{
    const formData = req.body
    const { data, error } = await supabase
        .from('events')
        .update({
            'e-name': formData['e-name'] ,
            'e-desc': formData['e-desc'],
            'sig': formData['sig'],
            'isDone': formData['isDone'],
            'isTech': formData['isTech'],
            'date': formData['date'],
        })
        .eq('id', formData['id'])

    if(error){
        console.log(error)
        return res.send("Error : " + error)
    }
    res.send("<script>" +
        "alert('Updated Successfully');" +
        "window.location.href = \"/\";"+
        "</script>")
})

//Remove the event
app.get('/removeevent',async (req,res)=>{
    const id = req.query.eventid
    const { error } = await supabase
        .from('events')
        .delete()
        .eq('id', id)

    if(error){
        console.log(error)
    }
    res.send("<script>" +
        "alert('Deleted Successfully');" +
        "window.location.href = \"/\";"+
        "</script>")

})

//Render page addEvent when user clicks on add member button
app.get('/addevent',async (req,res)=>{
    return res.render('addEvent.ejs')
})

//Add event to database
app.post('/addevent',async (req,res)=>{
    const formData = req.body
    const { data, error } = await supabase
        .from('events')
        .insert([{
            'e-name': formData['e-name'] ,
            'e-desc': formData['e-desc'],
            'sig': formData['sig'],
            'isDone': formData['isDone'],
            'isTech': formData['isTech'],
            'date': formData['date'],
        },
        ])
        .select()

    if(error){
        console.log(error)
        return res.send("Error : " + error)
    }
    res.send("<script>" +
        "alert('Added Successfully');" +
        "window.location.href = \"/\";"+
        "</script>")
})

//export the app variable
module.exports = app