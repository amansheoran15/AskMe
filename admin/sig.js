const express = require('express')

//Connecting to supabase
const {createClient} = require('@supabase/supabase-js')
const supabase = createClient('https://pjshkjaswzdtfuxpqxfr.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqc2hramFzd3pkdGZ1eHBxeGZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTc1NjEzNjEsImV4cCI6MjAxMzEzNzM2MX0.t_oXV-0P24Z1oFebdvzAdG-ujrN8vfJP1J2tbRlbkpk')

const app = express.Router()

async function getSpecificSIG(id){
    let { data: sig, error } = await supabase
        .from('sig')
        .select('*')
        .eq('id',id)
    if(error){
        console.log(error)
    }else{
        return sig
    }
}

//Render page editSig.ejs when user clicks the Edit button
app.get('/editsig',async (req, res) => {
    const sig = await getSpecificSIG(req.query.sigid)
    res.render('editSig',{
        row:sig
    })
})

//Update changes in the sig details
app.post('/editsig',async (req,res)=>{
    const formData = req.body
    const { data, error } = await supabase
        .from('sig')
        .update({
            'name': formData['name'] ,
            'desc': formData['desc'],
            'head': formData['head'],
            'alias': formData['alias']
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

//Remove the sig
app.get('/removesig',async (req,res)=>{
    const id = req.query.sigid
    const { error } = await supabase
        .from('sig')
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

//Render page addSig when user clicks on add member button
app.get('/addsig',async (req,res)=>{
    return res.render('addSig.ejs')
})

//Add SIG to database
app.post('/addsig',async (req,res)=>{
    const formData = req.body
    const { data, error } = await supabase
        .from('sig')
        .insert([{
            'name': formData['name'] ,
            'desc': formData['desc'],
            'head': formData['head'],
            'alias': formData['alias']
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

