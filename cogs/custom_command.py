import discord
from discord.ext import commands
from discord import app_commands
from config import TEST_GUILDS_ID, GUILDS_ID
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta, timezone

load_dotenv()

db_client = MongoClient(os.getenv("DB_CONNECT"))
db = db_client.custom_command_database

class CustomCommand(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="create", description="Create a custom command for you!")
    @app_commands.guilds(*GUILDS_ID)
    @app_commands.describe(name="Name of your command", text="The content of your command")
    async def create(self, interaction: discord.Interaction, name: str, text: str):
        guild_id = str(interaction.guild_id);
        
        collection = db[guild_id]
        
        if collection.find_one({"name": name}):
            await interaction.response.send_message(f"This command name is already existed, please choose another name or delete the old one!")
            return
        
        cmmd = {
            "name": name,
            "text": text,
            "author": {
            "id": interaction.user.id,
            "name": interaction.user.name,
            "display_name": interaction.user.display_name
            },
            "created_at": datetime.now(timezone(timedelta(hours=7))).isoformat()
        }
        
        collection.insert_one(cmmd)
        
        await interaction.response.send_message(f"Yay! Command created, to use your command, type `?{name}`")    
        
    
    @app_commands.command(name="delete", description="Delete a custom command for you!")
    @app_commands.guilds(*GUILDS_ID)
    @app_commands.describe(name="Name of your command that need to be deleted")
    async def delete(self, interaction: discord.Interaction, name: str):
        guild_id = str(interaction.guild_id);
        collection = db[guild_id]
        
        if not collection.find_one({"name": name}):
            await interaction.response.send_message("That command is not existed!")
            return
        
        collection.delete_one({"name": name})
        await interaction.response.send_message(f"Command ?{name} is successfully deleted!")
        return
    
    @app_commands.command(name="list", description="List every custom commands have created")
    @app_commands.guilds(*GUILDS_ID)
    async def list(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild_id)
        collection = db[guild_id]
        
        commands_list = ""
        for doc in collection.find():
            commands_list += f"?`{doc["name"]}`: `{doc["text"]}`\n\tcreated by: `{doc["author"]["name"]}`\n"
        await interaction.response.send_message(f"Aye! Verily, wait me a bit!! Here we go:\n{commands_list}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith('?'):
            guild_id = str(message.guild.id)
            collection = db[guild_id]
            
            name = message.content.split()[0][1:]
            
            cmmd = collection.find_one({"name": name});
            if cmmd:
                await message.channel.send(cmmd["text"])
                
    
async def setup(client):
    await client.add_cog(CustomCommand(client))
