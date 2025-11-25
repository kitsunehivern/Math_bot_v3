import discord
from discord.ext import commands
from discord import app_commands
from config import TEST_GUILDS_ID, GUILDS_ID



class Hello(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="hello", description="Say hi!!!")
    @app_commands.guilds(*TEST_GUILDS_ID)
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")
    
async def setup(client):
    await client.add_cog(Hello(client))