const express = require('express')

//To parse post request body
const bodyParser = require('body-parser');

//Connecting to supabase
const {createClient} = require('@supabase/supabase-js')
const supabase = createClient('https://pjshkjaswzdtfuxpqxfr.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqc2hramFzd3pkdGZ1eHBxeGZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc1NjEzNjEsImV4cCI6MjAxMzEzNzM2MX0.t_oXV-0P24Z1oFebdvzAdG-ujrN8vfJP1J2tbRlbkpk')

const eventRouter = require('./event')
const sigRouter = require('./sig')
const memberRouter = require('./member')

const app = express()

app.listen(3000,()=>{
    console.log("App started")
})

// Middleware to parse POST request body
app.use(bodyParser.urlencoded({ extended: true }));

//Specify directory from which static files will be served.
app.use(express.static(__dirname))

//Specify the view engine
app.set('view engine','ejs')

async function getAllEvents(){
    let { data: events, error } = await supabase
        .from('events')
        .select('*')

    if(error){
        console.log(error)
    }else{
        return events
    }
}


async function getAllSIGs(){
    let { data: sigs, error } = await supabase
        .from('sig')
        .select('*')
    if(error){
        console.log(error)
    }else{
        return sigs
    }
}

async function getAllMembers(){
    let { data: members, error } = await supabase
        .from('members')
        .select('*')
    if(error){
        console.log(error)
    }else{
        return members
    }
}

//Render index page with all the table details
app.get('/',async (req,res)=>{
    const events = await getAllEvents()
    const sig = await getAllSIGs()
    const members = await getAllMembers()
    return res.render('index.ejs',{
        title: "AskMe Bot Admin Panel",
        eventCount: Object.keys(events).length,
        events: events,
        sigCount: Object.keys(sig).length,
        sig:sig,
        memCount: Object.keys(members).length,
        mem:members
    })
})

//Routing to different files
app.use('/event',eventRouter)
app.use('/sig',sigRouter)
app.use('/member', memberRouter)





