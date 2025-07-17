import discord
from discord.ext import commands
from discord import app_commands


TEST_GUILDS_ID = discord.Object(id=1066207532374294558)

class Hello(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="hello", description="Say hi!!!")
    @app_commands.guilds(TEST_GUILDS_ID)
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi there!")
    
async def setup(client):
    await client.add_cog(Hello(client))