import discord
from discord.ext import commands
from discord import app_commands
from config import TEST_GUILDS_ID, GUILDS_ID



class Info(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    commands_list = [
        r"`\info` - Information about the bot",
        r"`\roll` - Roll dices"
    ]
    
    @app_commands.command(name="info", description="Information about the bot")
    @app_commands.guilds(*GUILDS_ID)
    async def mathBot(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Hi! I am Math Bot!", description="A version 2.0 of a bot developed by _HDH", color=discord.Colour.blue());
        embed.add_field(name="List of commands", value="\n".join(self.commands_list))
        embed.set_footer(text="The bot is currently in development, more commands is on the way!")
        await interaction.response.send_message(embed=embed)    
    
    
async def setup(client):
    await client.add_cog(Info(client))