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
    await message.channel.send(ans)

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
    await message.channel.send(ans)

  elif msg == "$get-event-u":
    response = supabase.table('events').select('*').eq('isDone',
                                                       False).execute()
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
    await message.channel.send(ans)

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
    await message.channel.send(ans)


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
