const express = require('express')

//Connecting to supabase
const {createClient} = require('@supabase/supabase-js')
const supabase = createClient('https://pjshkjaswzdtfuxpqxfr.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqc2hramFzd3pkdGZ1eHBxeGZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc1NjEzNjEsImV4cCI6MjAxMzEzNzM2MX0.t_oXV-0P24Z1oFebdvzAdG-ujrN8vfJP1J2tbRlbkpk')

const app = express.Router()

async function getSpecificMember(id){
    let { data: member, error } = await supabase
        .from('members')
        .select('*')
        .eq('id',id)
    if(error){
        console.log(error)
    }else{
        return member
    }
}

//Render page editMember.ejs when user clicks the Edit button
app.get('/editmember',async (req, res) => {
    const mem = await getSpecificMember(req.query.memid)
    res.render('editMember',{
        row:mem
    })
})

//Update changes in the member details
app.post('/editmember',async (req,res)=>{
    const formData = req.body
    const { data, error } = await supabase
        .from('members')
        .update({
            'name': formData['name'] ,
            'desig': formData['desig'],
            'sig': formData['sig'],
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

//Remove the member
app.get('/removemember',async (req,res)=>{
    const id = req.query.memid
    const { error } = await supabase
        .from('members')
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

//Render page addMember when user clicks on add member button
app.get('/addmember',async (req,res)=>{
    return res.render('addMember.ejs')
})

//Add member to database
app.post('/addmember',async (req,res)=>{
    const formData = req.body
    const { data, error } = await supabase
        .from('members')
        .insert([{
            'name': formData['name'] ,
            'desig': formData['desig'],
            'sig': formData['sig']
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

