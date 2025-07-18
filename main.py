import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from config import GUILDS_ID, TEST_GUILDS_ID

load_dotenv()

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        try:
            for guild in GUILDS_ID:
                synced = await self.tree.sync(guild=guild)
                print(f'Synced {len(synced)} commands to guild {guild.id}')
            
        except Exception as e:
            print(f'Error syncing commands: {e}')
    
    # async def on_message(self, message):
    #     if message.author == self.user:
    #         return
    #     if message.content.startswith('hello'):
    #         await message.channel.send(f'Hi there {message.author}')
    
    # async def on_reaction_add(self, reaction, user):
    #     await reaction.message.channel.send('You reacted!')

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

async def main():
    initial_extensions = []

    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            initial_extensions.append("cogs." + file_name[:-3])
    
    for extension in initial_extensions:
        await client.load_extension(extension)
        
if __name__ == "__main__":
    asyncio.run(main())
    
client.run(os.getenv("TOKEN"))

