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

ip_address = ec2_metadata.public_ipv4 or ec2_metadata.private_ipv4
region = ec2_metadata.region
avail_zone = ec2_metadata.availability_zone

@client.event 
async def on_ready(): 
    print("Logged in as a bot {0.user}".format(client))
    if ip_address and region and avail_zone:
        print(f"Your EC2 Data are as follows: IP Address: {ip_address}, Region: {region}, Availability Zone: {avail_zone}")
    else:
        print("Could not retrieve EC2_metadata.")

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
            jokes = ["Parallel lines have so much in common but it’s a shame they’ll never meet.", "A man walked into his house and was delighted when he discovered that someone had stolen all of his lamps.", "I have an inferiority complex, but it's not a very good one."] 
            await message.channel.send(random.choice(jokes)) 
        elif user_message.lower() == "tell me about my server!":
            if ip_address and region and avail_zone:
                await message.channel.send(f"Your EC2 Data are as follows: IP Address: {ip_address}, Region: {region}, Availability Zone: {avail_zone}")
            else:
                await message.channel.send("Sorry but I could not retrieve the EC2_metadata for this server.")
    
    await client.process_commands(message)

@client.command()
async def opgg(ctx, *, summoner: str):
    if summoner.count("#") == 1:
        encoded_summoner = summoner.replace("#", "-")
        await ctx.send(f'OPGG link for {summoner}: https://na.op.gg/summoner/userName={encoded_summoner}')
    else:
        await ctx.send("The correct format must be SummonerName#Tag, please try again.")
client.run(token)