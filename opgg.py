import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from ec2_metadata import ec2_metadata


load_dotenv('opgg.env')

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)
token = os.getenv('TOKEN')

@client.event 
async def on_ready(): 
    print("Logged in as a bot {0.user}".format(client))
    print(f"Your EC2 Data: {ec2_metadata.region}")

@client.event 
async def on_message(message): 

    username = str(message.author).split("#")[0] 
    channel = str(message.channel.name) 
    user_message = str(message.content) 
  
    print(f'Message {user_message} by {username} on {channel}') 
    if message.author == client.user: 
        return
  
    if channel == "bottest": 
        if user_message.lower() == "hello" or user_message.lower() == "hi": 
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye": 
            await message.channel.send(f'Bye {username}') 
        elif user_message.lower() == "tell me a joke": 
            jokes = ["test"] 
            await message.channel.send(random.choice(jokes)) 
    
    await client.process_commands(message)

@client.command()
async def opgg(ctx, *, summoner: str):
    encoded_summoner = summoner.replace("#", "-")
    await ctx.send(f'OPGG link for {summoner}: https://na.op.gg/summoner/userName={encoded_summoner}')
client.run(token)