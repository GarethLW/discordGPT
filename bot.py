import discord
import json
import responses
import os


async def send_message(message, user_message, is_private):
    try:

        filename = 'chatHist.json'

        if os.stat(filename).st_size == 0:
            data = {"array": [{"role": "system", "content": "You are a helpful assistant."}]}
            with open(filename, mode='w') as file:
                json.dump(data, file)

        with open(filename, mode='r') as file:
            msg = json.load(file)

        new_data = {"role": 'user', "content": "Username: "+message.author.name+" Message: "+user_message}

        msg['array'].append(new_data)

        with open(filename, mode='w') as file:
            json.dump(msg, file)

        with open(filename, mode='r') as file:
            msg = json.load(file)

        response = responses.handle_response(msg['array'])
        print("response" + response)
        new_data = {"role": "assistant", "content": response}
        msg['array'].append(new_data)

        with open('chatHist.json', mode='w') as file:
            json.dump(msg, file)

    
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = os.getenv('DiscordToken')
    
    intents = discord.Intents().all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    
    @client.event
    async def on_message(message):
        if message.author != client.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            print(f"{username} said: '{user_message}'({channel})")

            if len(user_message) > 0:
                if user_message[0] == '?':
                    user_message = user_message[1:]
                    await send_message(message, user_message, is_private=True)
                else: 
                    await send_message(message, user_message, is_private=False)


    client.run(TOKEN)