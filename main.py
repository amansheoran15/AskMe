import os

import discord
import json
from supabase import create_client, Client

url: str = os.environ["SUPABASE_URL"]
key: str = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  msg = message.content

  if message.author == client.user:
    return

  elif msg.startswith('$hello'):
    await message.channel.send('Hello!')

  elif msg == "$get-help":
    ans = "Use the following commands to access the information about Web Enthusiasts' Club:\n\n";
    ans += "1. **$get-event-p**             :      Display all the past events of WEC\n"
    ans += "2. **$get-event-p <sig>**  :      Display all the past events of particular SIG. <sig> can take value gdsc, algo, intel, system\n"
    ans += "3. **$get-event-u**             :      Display all the upcoming events of WEC\n"
    ans += "4. **$get-event-u <sig>**  :      Display all the upcoming events of particular SIG. <sig> can take value gdsc, algo, intel, system\n"
    ans += "5. **$get-event-nt**           :      Display all the non technical events of WEC\n"
    ans += "6. **$get-info**                     :      Display information about all SIGs in WEC\n"
    ans += "7. **$get-info <sig>**          :      Display information about particular SIG. <sig> can take value gdsc, algo, intel, system and wec\n"
    ans += "8. **$get-members**             :      Display all the members of WEC\n"
    ans += "9. **$get-members <sig>**  :      Display all the members of particular SIG. <sig> can take value gdsc, algo, intel, system\n"

    await message.channel.send(ans)

  elif msg == "$get-event-p":

    response = supabase.table('events').select('*').eq('isDone',
                                                       True).execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    # print(response_data)
    ans = ""
    counter = 1
    for event in response_data.get('data'):
      # print (event)
      temp = str(counter) + ". **" + event.get(
          'e-name') + "** \nDate: " + event.get('date') + "\n\n" + event.get(
              'e-desc')
      ans += temp + "\n\n"
      counter += 1
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]

  elif msg.startswith('$get-event-p'):
    sig = msg.split("$get-event-p ", 1)[1]
    response = supabase.table('events').select('*').eq('sig',
                                                       sig).eq('isDone',
                                                               True).execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    if (len(response_data.get('data')) == 0):
      return

    ans = ""
    counter = 1
    for event in response_data.get('data'):
      # print (event)
      temp = str(counter) + ". **" + event.get(
          'e-name') + "** \nDate: " + event.get('date') + "\n\n" + event.get(
              'e-desc')
      ans += temp + "\n\n"
      counter += 1
      
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]

  elif msg == "$get-event-u":
    response = supabase.table('events').select('*').eq('isDone',
                                                       False).execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    # print(response_data)
    ans = ""
    counter = 1
    for event in response_data.get('data'):

      temp = str(counter) + ". **" + event.get(
          'e-name') + "** \nDate: " + event.get('date') + "\n\n" + event.get(
              'e-desc')
      ans += temp + "\n\n"
      counter += 1
      
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]

  elif msg.startswith('$get-event-u'):
    sig = msg.split("$get-event-u ", 1)[1]
    response = supabase.table('events').select('*').eq('sig', sig).eq(
        'isDone', False).execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    if (len(response_data.get('data')) == 0):
      return

    ans = ""
    counter = 1
    for event in response_data.get('data'):
      # print (event)
      temp = str(counter) + ". **" + event.get(
          'e-name') + "** \nDate: " + event.get('date') + "\n\n" + event.get(
              'e-desc')
      ans += temp + "\n\n"
      counter += 1
      
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]

  elif msg == "$get-event-nt":
    response = supabase.table('events').select('*').eq('isTech',
                                                       False).execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    # print(response_data)
    ans = ""
    counter = 1
    for event in response_data.get('data'):
  
      temp = str(counter) + ". **" + event.get(
          'e-name') + "** \nDate: " + event.get('date') + "\n\n" + event.get(
              'e-desc')
      ans += temp + "\n\n"
      counter += 1
  
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]

  elif msg == '$get-info':
    response = supabase.table('sig').select('*').execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    if (len(response_data.get('data')) == 0):
      return
  
    ans = ""
    counter = 1;
    for event in response_data.get('data'):
      # print (event)
      temp =str(counter) +". **" + event.get(
          'name') + "**\n\n" + event.get(
              'desc')
      ans += temp + "\n\n"
      counter += 1
  
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]

  elif msg == '$get-info wec':
    ans = "**Web Enthusisats' Club** \n\nThis club is where you find all the computer science minds. It has four Special Interest Groups known as SIGs. These are\n1. **Algorithms**\n2. **Google Developer Students Clubs**\n3. **System & Security Group** \n4. **Intelligence Group**"

    await message.channel.send(ans)

  elif msg.startswith('$get-info'):
    sig = msg.split("$get-info ", 1)[1]
    response = supabase.table('sig').select('*').eq('alias', sig).execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    if (len(response_data.get('data')) == 0):
      return
  
    ans = ""
    for event in response_data.get('data'):
      # print (event)
      temp ="**" + event.get(
          'name') + "**\n\n" + event.get(
              'desc')
      ans += temp + "\n\n"

    await message.channel.send(ans)

  elif msg == '$get-members':
    response = supabase.table('members').select('*').execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    if (len(response_data.get('data')) == 0):
      return
  
    ans = ""
    counter = 1;
    for event in response_data.get('data'):
      # print (event)
      temp =str(counter) +". **" + event.get(
          'name') + "**\nDesignation : " + event.get(
              'desig')
      ans += temp + "\n\n"
      counter += 1
  
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]

  elif msg.startswith('$get-members'):
    sig = msg.split("$get-members ", 1)[1]
    response = supabase.table('members').select('*').eq('sig',sig).execute()
    response_str = response.model_dump_json()
    response_data = json.loads(response_str)
    if (len(response_data.get('data')) == 0):
      return
  
    ans = ""
    counter = 1;
    for event in response_data.get('data'):
      # print (event)
      temp =str(counter) +". **" + event.get(
          'name') + "**\nDesignation : " + event.get(
              'desig')
      ans += temp + "\n\n"
      counter += 1
  
    while ans:
      await message.channel.send(ans[:2000])
      ans = ans[2000:]


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
